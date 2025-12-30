from app.db.supabase_client import get_supabase
from langchain_openai import OpenAIEmbeddings

class VectorService:
    def __init__(self):
        self.client = get_supabase()
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    async def save_citation(self, project_id: str, title: str, abstract: str, url: str):
        # 1. Generate Embedding
        vector = await self.embeddings.aembed_query(abstract)
        
        # 2. Save to Supabase
        data = {
            "project_id": project_id,
            "title": title,
            "abstract": abstract,
            "url": url,
            "embedding": vector
        }
        response = self.client.table("citations").insert(data).execute()
        return response.data

    async def search_similar(self, project_id: str, query: str, limit: int = 5):
        # 1. Embed the query
        query_vector = await self.embeddings.aembed_query(query)
        
        # 2. Call Supabase RPC (Remote Procedure Call) for vector similarity
        # Note: You need to create this function in SQL (see below)
        params = {
            "query_embedding": query_vector,
            "match_threshold": 0.7,
            "match_count": limit,
            "p_id": project_id
        }
        response = self.client.rpc("match_citations", params).execute()
        return response.data