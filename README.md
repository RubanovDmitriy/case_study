# case_study

You are testing a decision making system.


If a rule is triggered, in the stop_factors field the name of the rule is written and in the decision field the status is "reject".
If not a single rule worked in the decision field the status is "approve".
If the rule worked and an exception was triggered, nothing is entered in the decision field and the rule name is entered in the stop_factors field.
You need to write test cases in pseudocode with a detailed description of each test and the expected result.

1. rule SC_B
if id = "6438Tty_4ff00278"
and
( (score <= 400)
    or
    (score <= 500 and items = "iphone, galaxy, redmi, poco" and amount > 200)
    or
    (score <= 550 and datediff(day,registered_since_at_store, ApplicationDate) <= 30 and amount > 200)
    or
    (score_v2 <= 250)

)
then decision = "reject" and stop_factors = "SC_B;"

Exceptions: risk_strategy_type in( 'light','middle') OR payment_is_test = "true" or product_type = 'card_installments' 


2. rule SC_N
if group_id = '6ef811855e53'
and item in ("video", "camera", "kitchen_dining", "bath", "baby_product")
and (	(score <= 350) or
        (score <= 400 and amount > 600) or
        (score <= 420 and amount > 1200) or
        (identity_score > 100 and amount > 750
        and score <= 420)
)
then decision = "reject" and stop_factors = 'SC_N;'


Exceptions: risk_strategy_type in( 'light','middle') OR payment_is_test = "true" or product_type = 'installments' 


Create tests in pseudocode is not fun, so I did more:

1. Implemented rules as python functions
2. Created parameterized test for this functions
3. Added comments for test cases according to which test design technics I used
4. Added coverage report in terminal
5. Dockerized it

Now you just need to:
1. Build docker image - docker build -t scoring_system .
2. Run - docker run scoring_system


