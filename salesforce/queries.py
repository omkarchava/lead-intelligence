from salesforce.sf_client import sf


def get_lead(lead_id):

    query = f"""
    SELECT
        Id,
        Name,
        Company,
        Industry,
        LeadSource,
        OwnerId
    FROM Lead
    WHERE Id = '{lead_id}'
    """

    result = sf.query(query)

    if result["totalSize"] == 0:
        return None

    return result["records"][0]