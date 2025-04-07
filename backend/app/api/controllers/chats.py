from fastapi import APIRouter

router = APIRouter()


@router.post("/chats")
def create_chat():
    pass


@router.get("/chats")
def get_chats():
    pass


@router.get("/chats/{chat_id}")
def get_chat():
    pass


@router.put("/chats/{chat_id}")
def update_chat():
    pass


@router.delete("/chats/{chat_id}")
def delete_chat():
    pass
