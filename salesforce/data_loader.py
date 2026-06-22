from salesforce.sf_client import sf

def get_leads():

    return sf.query("""
        SELECT
            Id,
            Industry,
            LeadSource,
            Status,
            OwnerId
        FROM Lead
    """)

def get_opportunities():

    return sf.query("""
        SELECT
            Id,
            Amount,
            StageName,
            OwnerId,
            IsWon,
            IsClosed,
            CreatedDate,
            CloseDate
        FROM Opportunity
    """)

def get_users():

    return sf.query("""
        SELECT
            Id,
            Name,
            Department,
            Title
        FROM User
        WHERE IsActive = true
    """)

def get_accounts():

    return sf.query("""
        SELECT
            Id,
            Industry
        FROM Account
    """)