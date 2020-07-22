import stripe
import json
import interface as inter

stripe.api_key = "sk_test_dapedBnAMB6uk0EtabwAZTn800Dp0xgRzr"


def new_user(userid, email):
    acct = stripe.Customer.create(email=email)
    acct_id = acct["id"]
    intent = stripe.SetupIntent.create(customer=acct_id)
    # backend can now create card for defined user
    query = f"INSERT INTO stripe VALUES (\'{userid}\', \'{acct_id}\')"
    return inter.execute_query(query)


def charge_card(card_id):
    resp = stripe.Charge.create(amount=5000, currency="usd", source="tok-visa")


def get_card_options(userid):
    query = f"SELECT stripe_id FROM stripe WHERE id = \'{userid}\'"
    data = inter.execute_read_query(query)
    customer_id = data[0][0]

new_user(1, "ecl.damoos@gmail.com")
get_card_options(1)

# need to create payment intent object
"""
try:
  stripe.PaymentIntent.create(
    amount=1099,
    currency='usd',
    customer='{{CUSTOMER_ID}}',
    payment_method='{{PAYMENT_METHOD_ID}}',
    off_session=True,
    confirm=True,
  )
except stripe.error.CardError as e:
  err = e.error
  """