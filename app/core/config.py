from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str  # Use the "service_role" key for backend, "anon" for frontend
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()