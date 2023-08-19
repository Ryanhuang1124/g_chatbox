from fastapi import APIRouter

router = APIRouter(
    tags=['record'],
    prefix='/record'
)


@router.get("/")
def get_all_auth():
    return {"":""}