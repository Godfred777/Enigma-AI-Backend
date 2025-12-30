from app.db.supabase_client import get_supabase
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

class VectorService:
    def __init__(self):
        self.client = get_supabase()
        # Ensure this matches the dimensions of your vector column (1536 for OpenAI)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    async def save_citation(self, project_id: str, title: str, abstract: str, url: str):
        """
        Embeds the abstract and saves the citation to Supabase in one go.
        """
        # 1. Create the vector
        vector = await self.embeddings.aembed_query(abstract)
        
        # 2. Insert into Supabase 'citations' table
        data = {
            "project_id": project_id,
            "title": title,
            "abstract": abstract,
            "url": url,
            "embedding": vector  # pgvector handles the list[float] automatically
        }
        
        # We use .execute() to run the query immediately
        try:
            response = self.client.table("citations").insert(data).execute()
            return response.data[0]
        except Exception as e:
            # Log this error in production
            print(f"Error saving citation: {e}")
            return None

    async def search_similar(self, project_id: str, query: str, limit: int = 5):
        """
        Finds relevant papers using the 'match_citations' RPC function we wrote in SQL.
        """
        query_vector = await self.embeddings.aembed_query(query)
        
        params = {
            "query_embedding": query_vector,
            "match_threshold": 0.5, # Adjust this: 0.7 is strict, 0.5 is loose
            "match_count": limit,
            "p_id": project_id
        }
        
        # Call the PostgreSQL function directly
        response = self.client.rpc("match_citations", params).execute()
        
        # Convert to LangChain Documents for your Agents
        documents = []
        for item in response.data:
            doc = Document(
                page_content=item['abstract'],
                metadata={"title": item['title'], "id": item['id'], "score": item['similarity']}
            )
            documents.append(doc)
            
        return documents