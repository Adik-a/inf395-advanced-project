from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from database import SessionDep
from auth import get_current_user

from modules.messages.repository import MessagesRepository
from modules.messages.schemas import MessagesSchema

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/{user_email}")
async def get_messages(
    user_email: str,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    messages = await MessagesRepository.get_messages_between_users(
        user1_id=current_user["sub"],
        user2_email=user_email,
        session=session,
    )
    return messages


@router.get("/my/all")
async def get_all_messages(
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    messages = await MessagesRepository.get_my_all_messages(
        user_id=current_user["sub"],
        session=session,
    )
    return messages


@router.get("/get-id-by-email/{email}")
async def get_user_id_by_email(
    email: str,
    session: SessionDep,
):
    user = await MessagesRepository.get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id}


@router.post("/send")
async def send_message(
    data: MessagesSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    new_message = await MessagesRepository.create_message(
        sender_id=current_user["sub"],
        receiver_email=data.receiver_email,
        content=data.content,
        session=session,
    )
    return new_message


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_private_message(self, message: dict, target_id: int):
        websocket = self.active_connections.get(target_id)
        if websocket:
            await websocket.send_json(message)
        else:
            # Тут можно логику: сохранить в БД, если юзер офлайн
            print(f"Пользователь {target_id} не в сети")


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    user_id: int,
    websocket: WebSocket,
    session: SessionDep,
):
    await manager.connect(user_id, websocket)
    try:
        while True:
            # Ожидаем JSON формат: {"receiver_id": 2, "message": "Привет!"}
            data = await websocket.receive_json()

            receiver_id = data.get("receiver_id")
            content = data.get("message")

            new_message = await MessagesRepository.create_message(
                user_id,
                int(receiver_id),
                content,
                session,
            )

            payload = {
                "id": new_message.id,
                "sender_id": user_id,
                "content": content,
                "created_at": str(new_message.created_at),
            }

            # Отправляем сообщение получателю
            await manager.send_private_message(payload, int(receiver_id))

            # (Опционально) Отправляем отправителю подтверждение
            # await manager.send_private_message(payload, user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
