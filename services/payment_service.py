from fastapi import APIRouter

router = APIRouter()


@router.post("/init")
def initiate_payment():
    pass


@router.post("/verify")
def verify_payment():
    pass
