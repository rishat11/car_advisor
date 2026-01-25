from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user import ChatService
from app.core.security import get_current_user
from app.schemas.user import ChatRequest, ChatResponse, SuccessResponse


router = APIRouter()
chat_service = ChatService()


@router.post("/send", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        response = await chat_service.process_chat_request(db, current_user.id, chat_request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")


@router.get("/sessions", response_model=list[dict])
async def get_user_sessions(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    sessions = await chat_service.get_user_sessions(db, current_user.id)
    return [
        {
            "id": session.id,
            "title": session.title,
            "created_at": session.created_at,
            "updated_at": session.updated_at
        }
        for session in sessions
    ]


@router.get("/sessions/{session_id}/messages", response_model=list[dict])
async def get_session_messages(
    session_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify that the session belongs to the current user
    session = await chat_service.get_session_by_id(db, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = await chat_service.get_session_messages(db, session_id)
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "role": msg.role,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]