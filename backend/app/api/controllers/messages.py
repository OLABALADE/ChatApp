from fastapi import APIRouter

router = APIRouter()


@router.post("/chats/{chat_id}/messages")
def create_message():
    pass


@router.get("/chat/{chat_id}/messages")
def get_messages():
    pass


@router.get("/chat/{chat_id}/messages/{message_id}")
def get_message():
    pass


@router.put("/chat/{chat_id}/messages/{message_id}")
def update_message():
    pass


@router.delete("/chat/{chat_id}/messages/{message_id}")
def delete_message():
    pass
