from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.config.env')
    
    BASE_DIR: str
    MEDIA: str
    PINECONE_API_KEY: str


settings = Settings()