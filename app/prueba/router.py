from fastapi import  APIRouter, Depends
from auth.dependencies import RoleChecker

allow_create_resource = RoleChecker(["std"])


router = APIRouter(
    prefix="/prueba",
    responses={404: {"description": "Not found"}},
    #dependencies=[Depends(get_current_active_user)],
    dependencies=[Depends(allow_create_resource)],
)


@router.get("/")
async def read_users_me():
    return {'bla':7}


