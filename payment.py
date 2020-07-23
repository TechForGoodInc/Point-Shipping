import stripe
import json
import interface as inter

stripe.api_key = "sk_test_dapedBnAMB6uk0EtabwAZTn800Dp0xgRzr"


def new_user(userid, email):
    acct = stripe.Customer.create(email=email)
    acct_id = acct["id"]
    intent = stripe.SetupIntent.create(customer=acct_id)
    # stripe.Customer.create_source(acct_id, source={card number})
    # backend can now create card for defined user
    query = f"INSERT INTO stripe VALUES (\'{userid}\', \'{acct_id}\')"
    return inter.execute_query(query)


def get_id(userid):
    query = f"SELECT stripe_id FROM stripe WHERE id = \'{userid}\'"
    data = inter.execute_read_query(query)
    if data:
        return data[0][0]
    else:
        return False


def charge_card(amount, card_id, userid):
    try:
        query = f"SELECT stripe_id FROM stripe WHERE id = \'{userid}\'"
        data = inter.execute_read_query(query)
        if data:
            customer_id = data[0][0]
            intent = stripe.PaymentIntent.create(amount=amount, currency='usd',
                                                 customer=f"{customer_id}",
                                                 payment_method=f"{card_id}",
                                                 off_session=False,
                                                 confirm=True)
        else:
            return "False"
    except stripe.error.CardError as e:
        return e.err
    # now backend can charge the card
    return intent


def get_card_options(userid):
    query = f"SELECT stripe_id FROM stripe WHERE id = \'{userid}\'"
    data = inter.execute_read_query(query)
    if data:
        customer_id = data[0][0]
        return stripe.PaymentMethod.list(customer=f"{customer_id}",
                                         type="card")
