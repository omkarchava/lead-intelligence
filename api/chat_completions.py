from fastapi import APIRouter
from fastapi import Depends

from security import verify_api_key

router = APIRouter()


@router.post("/chat/completions")
def chat_completions(
    payload: dict,
    auth=Depends(
        verify_api_key
    )
):

    messages = payload.get(
        "messages",
        []
    )

    user_message = ""

    if len(messages) > 0:

        user_message = messages[-1].get(
            "content",
            ""
        )

    return {

        "id":
            "lead-intelligence",

        "object":
            "chat.completion",

        "created":
            1710000000,

        "model":
            "Lead-Intelligence-v1",

        "choices": [

            {
                "index": 0,

                "message": {

                    "role":
                        "assistant",

                    "content":
                        f"You said: {user_message}"

                },

                "finish_reason":
                    "stop"

            }

        ]
    }