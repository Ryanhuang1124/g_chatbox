from fastapi import APIRouter

router = APIRouter(
    tags=['conversation'],
    prefix='/conversation'
)


@router.get("/")
def get_all_auth():
    return {"":""}