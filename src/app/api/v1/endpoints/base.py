from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def onboard_message():
    return {"message": "You've been onboarded!"}