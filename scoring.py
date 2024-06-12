from datetime import datetime


def rule_sc_b(
    id: str,
    score: int,
    items: str,
    amount: int,
    score_v2: int,
    application_date: datetime,
    registered_since_at_store: datetime,
    risk_strategy_type: str,
    payment_is_test: bool,
    product_type: str,
) -> dict[str, str]:
    """Evaluate rule SC_N and return decision and stop factors."""

    if risk_strategy_type in ["light", "middle"] or payment_is_test is True or product_type == "card_installments":
        return {"decision": "", "stop_factors": ""}

    if id == "6438Tty_4ff00278" and (
        score <= 400
        or (score <= 500 and items == "iphone, galaxy, redmi, poco" and amount > 200)
        # items == "iphone, galaxy, redmi, poco" this condition is strange,
        # I would like to ask maybe we need list of items here
        or (score <= 550 and (application_date - registered_since_at_store).days <= 30 and amount > 200)
        or score_v2 <= 250
    ):
        return {"decision": "reject", "stop_factors": "SC_B;"}

    return {"decision": "approve", "stop_factors": ""}


def rule_sc_n(
    group_id: str,
    item: str,
    score: int,
    amount: int,
    identity_score: int,
    risk_strategy_type: int,
    payment_is_test: bool,
    product_type: str,
) -> dict[str, str]:
    """Evaluate rule SC_N and return decision and stop factors."""

    # Check for exceptions
    if risk_strategy_type in ["light", "middle"] or payment_is_test is True or product_type == "installments":
        return {"decision": "", "stop_factors": ""}

    # Evaluate the rule
    if group_id == "6ef811855e53" and item in ["video", "camera", "kitchen_dining", "bath", "baby_product"]:
        if (
            score <= 350
            or (
                score <= 400 and amount > 600
            )   # we do not need to test this condition
                # because it is the same equivalence class as (score <= 420 and amount > 1200)
            or (score <= 420 and amount > 1200)
            or (identity_score > 100 and amount > 750 and score <= 420)
        ):
            return {"decision": "reject", "stop_factors": "SC_N;"}

    return {"decision": "approve", "stop_factors": ""}