import re

from fastapi import APIRouter
from fastapi import Depends

from security import verify_api_key

from salesforce.sf_client import sf
from salesforce.pincode_loader import get_reps_by_pincode

from services.recommendation_service import (
    get_recommendations
)

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

    if len(messages) == 0:

        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "No prompt received."
                    }
                }
            ]
        }

    prompt = messages[-1].get(
        "content",
        ""
    )

    lead_match = re.search(
        r"00Q[a-zA-Z0-9]{12,15}",
        prompt
    )

    if not lead_match:

        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content":
                            "Lead Id not found."
                    }
                }
            ]
        }

    lead_id = lead_match.group()

    lead_query = f"""
    SELECT
        Id,
        Name,
        Pincode__c
    FROM Lead
    WHERE Id = '{lead_id}'
    LIMIT 1
    """

    lead_result = sf.query(
        lead_query
    )

    if len(
        lead_result["records"]
    ) == 0:

        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content":
                            "Lead not found."
                    }
                }
            ]
        }

    lead = lead_result[
        "records"
    ][0]

    pincode = str(
        int(
            float(
                lead["Pincode__c"]
            )
        )
    )

    reps = get_reps_by_pincode(
        pincode
    )

    rep_ids = [
        r["User__c"]
        for r in reps
        if r.get("User__c")
    ]

    recommendations = (
        get_recommendations(
            rep_ids
        )
    )

    if len(recommendations) == 0:

        result_text = (
            "No recommendations found."
        )

    else:

        best = recommendations[0]

        result_text = f"""
Lead: {lead['Name']}

Recommended Owner:
{best['rep_name']}

Assignment Score:
{best.get('assignment_score',0)}

Estimated Days:
{best.get('estimated_days',0)}

Capacity Score:
{best.get('capacity_score',0)}

Win Rate:
{best.get('win_rate',0)}%
"""

    return {

        "id":
            "lead-intelligence",

        "object":
            "chat.completion",

        "model":
            "Lead-Intelligence-v1",

        "choices": [

            {
                "index": 0,

                "message": {

                    "role":
                        "assistant",

                    "content":
                        result_text

                },

                "finish_reason":
                    "stop"

            }

        ]
    }