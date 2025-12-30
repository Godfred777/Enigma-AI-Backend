from supabase import create_client, Client
from app.core.config import settings

supabase_client: Client = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_KEY
)

def get_supabase_client() -> Client:
    return supabase_client