"""
You are testing a decision-making system.
If a rule is triggered, in the stop_factors field the name of the rule is written and in the decision field the
status is "reject".
If not a single rule worked in the decision field the status is "approve".
If the rule worked and an exception was triggered, nothing is entered in the decision field and the rule name
is entered in the stop_factors field.
You need to write test cases in pseudocode with a detailed description of each test and the expected result.
"""

import pytest
from datetime import datetime

from scoring_system.scoring import rule_sc_b, rule_sc_n


@pytest.mark.parametrize(
    "id, score, items, amount, score_v2, application_date, registered_since_at_store, risk_strategy_type, "
    "payment_is_test, product_type, return_value",
    [
        (
            "test_pass",
            501,
            "",
            201,
            251,
            datetime(2024, 3, 1),
            datetime(2024, 1, 1),
            "",
            False,
            "",
            {"decision": "approve", "stop_factors": ""},
        ),  # happy pass for different id
        (
            "6438Tty_4ff00278",
            501,
            "",
            201,
            251,
            datetime(2024, 3, 1),
            datetime(2024, 1, 1),
            "",
            False,
            "",
            {"decision": "approve", "stop_factors": ""},
        ),  # happy pass boundary values for score
        (
            "test_exc_rst_light",
            0,
            "",
            0,
            0,
            datetime(2024, 1, 1),
            datetime(2024, 1, 1),
            "light",
            False,
            "",
            {"decision": "", "stop_factors": ""},
        ),  # test light risk_strategy_type exception
        (
            "test_exc_rst_middle",
            0,
            "",
            0,
            0,
            datetime(2024, 1, 1),
            datetime(2024, 1, 1),
            "middle",
            False,
            "",
            {"decision": "", "stop_factors": ""},
        ),  # test middle risk_strategy_type exception
        (
            "test_exc_payment_is_test",
            0,
            "",
            0,
            0,
            datetime(2024, 1, 1),
            datetime(2024, 1, 1),
            "",
            True,
            "",
            {"decision": "", "stop_factors": ""},
        ),  # test payment_is_test is True exception
        (
            "test_exc_pt_card_installments",
            0,
            "",
            0,
            0,
            datetime(2024, 1, 1),
            datetime(2024, 1, 1),
            "",
            False,
            "card_installments",
            {"decision": "", "stop_factors": ""},
        ),  # test product_type == 'card_installments'
        (
            "6438Tty_4ff00278",
            400,
            "",
            201,
            251,
            datetime(2024, 3, 1),
            datetime(2024, 1, 1),
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_B;"},
        ),  # test score <= 400
        (
            "6438Tty_4ff00278",
            500,
            "iphone, galaxy, redmi, poco",
            201,
            251,
            datetime(2024, 1, 1),
            datetime(2024, 1, 1),
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_B;"},
        ),  # test score <= 500 and items == "iphone, galaxy, redmi, poco" and amount > 200
        (
            "6438Tty_4ff00278",
            550,
            "",
            201,
            251,
            datetime(2024, 1, 30),
            datetime(2024, 1, 1),
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_B;"},
        ),  # test score <= 550 and (application_date - registered_since_at_store).days <= 30 and amount > 200
        (
            "6438Tty_4ff00278",
            501,
            "",
            201,
            250,
            datetime(2024, 3, 1),
            datetime(2024, 1, 1),
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_B;"},
        ),  # test score_v2 <= 250
    ],
)
def test_rule_sc_b(
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
    return_value: dict[str, str],
) -> None:
    assert (
        rule_sc_b(
            id,
            score,
            items,
            amount,
            score_v2,
            application_date,
            registered_since_at_store,
            risk_strategy_type,
            payment_is_test,
            product_type,
        )
        == return_value
    )


@pytest.mark.parametrize(
    "group_id, item, score, amount, identity_score, risk_strategy_type, payment_is_test, product_type, return_value",
    [
        (
            "6ef811855e53",
            "baby_product",
            421,
            600,
            100,
            "",
            False,
            "",
            {"decision": "approve", "stop_factors": ""},
        ),  # test happy_path
        (
            "",
            "",
            421,
            600,
            100,
            "light",
            False,
            "",
            {"decision": "", "stop_factors": ""},
        ),  # test exception risk_strategy_type light
        (
            "",
            "",
            421,
            600,
            100,
            "middle",
            False,
            "",
            {"decision": "", "stop_factors": ""},
        ),  # test exception risk_strategy_type middle
        ("", "", 421, 600, 100, "", True, "", {"decision": "", "stop_factors": ""}),  # test payment_is_test is True
        (
            "",
            "",
            421,
            600,
            100,
            "",
            False,
            "installments",
            {"decision": "", "stop_factors": ""},
        ),  # test product_type == installments
        (
            "6ef811855e53",
            "video",
            350,
            600,
            100,
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_N;"},
        ),  # test score <= 350 with item video
        (
            "6ef811855e53",
            "bath",
            350,
            600,
            100,
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_N;"},
        ),  # test score <= 350 with item bath
        (
            "6ef811855e53",
            "camera",
            420,
            1201,
            100,
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_N;"},
        ),  # test score <= 420 and amount > 1200 with item camera
        (
            "6ef811855e53",
            "kitchen_dining",
            420,
            751,
            101,
            "",
            False,
            "",
            {"decision": "reject", "stop_factors": "SC_N;"},
        ),  # test identity_score > 100 and amount > 750 and score <= 420
    ],
)
def test_rule_sc_n(
    group_id: str,
    item: str,
    score: int,
    amount: int,
    identity_score: int,
    risk_strategy_type: int,
    payment_is_test: bool,
    product_type: str,
    return_value: dict[str, str],
) -> None:
    assert (
        rule_sc_n(group_id, item, score, amount, identity_score, risk_strategy_type, payment_is_test, product_type)
        == return_value
    )
