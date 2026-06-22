from salesforce.sf_client import sf


def get_rep_metrics(rep_id):

    leads = sf.query(f"""
    SELECT Id
    FROM Lead
    WHERE OwnerId = '{rep_id}'
    AND IsConverted = false
    """)

    opps = sf.query(f"""
    SELECT
        Id,
        Amount,
        IsWon,
        IsClosed
    FROM Opportunity
    WHERE OwnerId = '{rep_id}'
    """)

    tasks = sf.query(f"""
    SELECT Id
    FROM Task
    WHERE OwnerId = '{rep_id}'
    AND Status != 'Completed'
    """)

    events = sf.query(f"""
    SELECT Id
    FROM Event
    WHERE OwnerId = '{rep_id}'
    """)

    active_leads = len(
        leads.get("records", [])
    )

    open_tasks = len(
        tasks.get("records", [])
    )

    upcoming_events = len(
        events.get("records", [])
    )

    opp_records = opps.get(
        "records",
        []
    )

    total_opps = len(
        opp_records
    )

    won_opps = len(
        [
            o
            for o in opp_records
            if o.get("IsWon")
        ]
    )

    open_opps = len(
        [
            o
            for o in opp_records
            if not o.get("IsClosed")
        ]
    )

    revenue = sum(
        float(
            o.get("Amount") or 0
        )
        for o in opp_records
    )

    win_rate = 0

    if total_opps > 0:

        win_rate = (
            won_opps
            /
            total_opps
        ) * 100

    capacity_score = max(
        0,
        100
        -
        (
            active_leads * 2
            +
            open_opps * 5
            +
            open_tasks * 1
            +
            upcoming_events * 2
        )
    )

    estimated_days = round(
        2
        +
        (active_leads * 0.5)
        +
        (open_opps * 1.5)
        +
        (open_tasks * 0.2)
        +
        (upcoming_events * 0.3),
        1
    )

    rep_score = round(
        (
            win_rate * 0.7
        )
        +
        (
            capacity_score * 0.3
        ),
        2
    )

    assignment_score = round(
        (
            rep_score
            *
            capacity_score
        ) / 100,
        2
    )

    return {
        "rep_id": rep_id,
        "rep_score": rep_score,
        "assignment_score":
            assignment_score,
        "estimated_days":
            estimated_days,
        "capacity_score":
            capacity_score,
        "win_rate":
            round(win_rate, 2),
        "revenue":
            revenue,
        "active_leads":
            active_leads,
        "open_opps":
            open_opps,
        "open_tasks":
            open_tasks,
        "upcoming_events":
            upcoming_events
    }


def get_recommendations(
    candidate_rep_ids
):

    recommendations = []

    for rep_id in candidate_rep_ids:

        try:

            user_result = sf.query(f"""
            SELECT
                Id,
                Name
            FROM User
            WHERE Id = '{rep_id}'
            LIMIT 1
            """)

            rep_name = rep_id

            if (
                "records"
                in user_result
                and
                len(
                    user_result["records"]
                ) > 0
            ):

                rep_name = (
                    user_result["records"][0]
                    .get("Name")
                )

            metrics = (
                get_rep_metrics(
                    rep_id
                )
            )

            metrics[
                "rep_name"
            ] = rep_name

            recommendations.append(
                metrics
            )

        except Exception as e:

            print(
                f"Error for rep "
                f"{rep_id}: {e}"
            )

    recommendations.sort(
        key=lambda x:
        x["assignment_score"],
        reverse=True
    )

    return recommendations