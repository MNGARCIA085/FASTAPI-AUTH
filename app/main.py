from fastapi import FastAPI, APIRouter
from auth import router as auth_routes
from prueba import router as prueba_routes


#models.Base.metadata.create_all(bind=engine); migrar sin usar alembic

app = FastAPI()


router = APIRouter()

app.include_router(auth_routes.router,tags=['auth'])
app.include_router(prueba_routes.router,tags=['prueba'])