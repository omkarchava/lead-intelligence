from fastapi import APIRouter

from salesforce.sf_client import sf
from salesforce.pincode_loader import get_reps_by_pincode

from fastapi import Depends
from security import verify_api_key

from services.recommendation_service import (
    get_recommendations
)

router = APIRouter()


@router.post("/recommend")
def recommend(
    payload: dict,
    auth=Depends(
        verify_api_key
    )):
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

    print("Lead Query Result:")
    print(lead_result)

    if (
        "records" not in lead_result
        or len(lead_result["records"]) == 0
    ):

        return {
            "success": False,
            "message": "Lead not found"
        }

    lead = lead_result["records"][0]

    raw_pincode = lead.get(
        "Pincode__c"
    )

    if not raw_pincode:

        return {
            "success": False,
            "message": "Lead Pincode not available"
        }

    try:

        pincode = str(
            int(float(raw_pincode))
        )

    except:

        pincode = str(
            raw_pincode
        ).strip()

    print(
        f"Lead Pincode: {pincode}"
    )

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

    print(
        "Candidate Reps:",
        rep_ids
    )

    recommendations = (
        get_recommendations(
            rep_ids
        )
    )

    conversion_probability = 75

    predicted_days = None
    if len(recommendations) > 0:
        predicted_days = recommendations[0][
        "estimated_days"
    ]

    recommended_owner = None

    if len(recommendations) > 0:

        recommended_owner = (
            recommendations[0]["rep_id"]
        )

    return {
        "success": True,
        "lead_id": lead_id,
        "lead_name": lead.get(
            "Name"
        ),
        "pincode": pincode,
        "recommended_owner":
            recommended_owner,
        "conversion_probability":
            conversion_probability,
        "predicted_days":
            predicted_days,
        "total_reps":
            len(recommendations),
        "recommendations":
            recommendations
    }