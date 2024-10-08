from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: int
    mysql_db: str
    secret_key: str
    algorithm: str
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    from_email: str

    model_config = SettingsConfigDict(env_file='.env')
    

settings = Settings(_env_file='.env')
