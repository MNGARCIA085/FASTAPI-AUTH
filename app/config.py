from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = "some mail"
    DB_USER:str
    DB_URL:str
    DB_URL_TEST:str
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    

    class Config:
        env_file = ".env"


settings = Settings()



"""

gnerar la secret key

# to get a string like this run:
# openssl rand -hex 32

"""