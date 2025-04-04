from ..schemas.messages import SupportMessageSchema
from ..utils.tasks import send_support_msg_to_bot
from fastapi import status, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from ..config.logger_config import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.post("")
async def send_msg_to_support(background_tasks: BackgroundTasks, message: SupportMessageSchema):
    """
    send msg to admin telegram
    """
    logger.info(f'get message from user : ""')

    background_tasks.add_task(send_support_msg_to_bot, message)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Your support request has been queued",
            "details": {
                "username": message.username,
            },
        },
    )
