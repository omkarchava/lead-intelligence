from fastapi import APIRouter
from fastapi import Depends

from security import verify_api_key

from salesforce.sf_client import sf
from salesforce.pincode_loader import get_reps_by_pincode

from services.recommendation_service import (
    get_recommendations
)

router = APIRouter()


@router.post("/predict")
def predict(
    payload: dict,
    auth=Depends(
        verify_api_key
    )
):

    if "lead_id" not in payload:

        return {
            "success": False,
            "message": "lead_id is required"
        }

    lead_id = payload["lead_id"]

    lead_query = f"""
    SELECT
        Id,
        Name,
        Pincode__c,
        LeadSource,
        Industry
    FROM Lead
    WHERE Id = '{lead_id}'
    LIMIT 1
    """

    lead_result = sf.query(
        lead_query
    )

    if (
        "records" not in lead_result
        or len(
            lead_result["records"]
        ) == 0
    ):

        return {
            "success": False,
            "message": "Lead not found"
        }

    lead = (
        lead_result["records"][0]
    )

    raw_pincode = lead.get(
        "Pincode__c"
    )

    if not raw_pincode:

        return {
            "success": False,
            "message":
                "Lead Pincode not available"
        }

    try:

        pincode = str(
            int(
                float(raw_pincode)
            )
        )

    except:

        pincode = str(
            raw_pincode
        ).strip()

    candidate_reps = (
        get_reps_by_pincode(
            pincode
        )
    )

    if not candidate_reps:

        return {
            "success": False,
            "message":
                f"No reps mapped for pincode {pincode}"
        }

    rep_ids = []

    for rep in candidate_reps:

        if rep.get("User__c"):

            rep_ids.append(
                rep["User__c"]
            )

    recommendations = (
        get_recommendations(
            rep_ids
        )
    )

    if len(recommendations) == 0:

        return {
            "success": False,
            "message":
                "No recommendations found"
        }

    best_rep = (
        recommendations[0]
    )

    return {

        "predictions": [

            {

                "lead_id":
                    lead_id,

                "lead_name":
                    lead.get("Name"),

                "recommended_owner":
                    best_rep["rep_id"],

                "recommended_owner_name":
                    best_rep["rep_name"],

                "assignment_score":
                    best_rep.get(
                        "assignment_score",
                        0
                    ),

                "rep_score":
                    best_rep.get(
                        "rep_score",
                        0
                    ),

                "predicted_days":
                    best_rep.get(
                        "estimated_days",
                        0
                    ),

                "win_rate":
                    best_rep.get(
                        "win_rate",
                        0
                    ),

                "capacity_score":
                    best_rep.get(
                        "capacity_score",
                        0
                    )

            }

        ],

        "all_recommendations":
            recommendations
    }