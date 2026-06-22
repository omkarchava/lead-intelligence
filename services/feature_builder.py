from salesforce.sf_client import sf


def build_rep_features(
    user_id
):

    opp_query = f"""
    SELECT
        Id,
        IsWon,
        Amount
    FROM Opportunity
    WHERE OwnerId = '{user_id}'
    """

    opps = sf.query_all(
        opp_query
    )["records"]

    total = len(opps)

    won = len(
        [
            o
            for o in opps
            if o["IsWon"]
        ]
    )

    win_rate = 0

    if total > 0:
        win_rate = won / total

    return {
        "win_rate": win_rate,
        "open_opps": total
    }