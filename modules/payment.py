import stripe
import json
import interface as inter

stripe.api_key = "sk_test_dapedBnAMB6uk0EtabwAZTn800Dp0xgRzr"


# customer's metadata will contain IDs of their charges (added
# manually by us)
def new_user(userid, email):
    acct = stripe.Customer.create(email=email)
    acct_id = acct["id"]
    query = f"INSERT INTO stripe VALUES (\'{userid}\', \'{acct_id}\')"
    return inter.execute_query(query)


def get_customer_id(userid):
    query = f"SELECT stripe_id FROM stripe WHERE id = \'{userid}\'"
    data = inter.execute_read_query(query)
    if data:
        return data[0][0]
    else:
        return False


def get_payment_options(userid):
    customer = stripe.Customer.retrieve(userid)
    payment_options = customer["sources"]
    return payment_options["data"]


# adds payment method (credit card) with option of making the 
# payment method the default card
def add_payment_method(customer_id, card_num, exp, cv, default=False):
    if default:
        customer = stripe.Customer.retrieve(customer_id)
        old_default = customer["default_source"]
        resp = stripe.Customer.modify(customer_id, default_source=pm_source)
        pm_source = old_default
        print(resp)
    resp = stripe.Customer.create_source(customer_id, source=pm_source)
    print(resp)


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
