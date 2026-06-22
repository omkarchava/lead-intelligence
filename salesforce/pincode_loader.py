from salesforce.sf_client import sf

def get_reps_by_pincode(pincode):

    try:
        pincode = str(
            int(float(pincode))
        )
    except:
        pincode = str(pincode).strip()

    query = f"""
    SELECT
        Id,
        Pincode__c,
        User__c,
        Priority__c
    FROM Pincode__c
    WHERE Pincode__c = '{pincode}'
    """

    print("Searching Pincode:", pincode)

    result = sf.query(query)

    print("Pincode Query Result:")
    print(result)

    if "records" not in result:
        return []

    return result["records"]