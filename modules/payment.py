import stripe
import json
import interface as inter

stripe.api_key = "sk_test_51H60XYAzJnRyZcvUC1Fanr3dfwLFo6XR1Ne1wq231HFeev2813AaQZXHQQWSrv2NT3jnwUqrqDapYvivHoMr051l00tz2S4nM2"

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
def add_payment_method(customer_id, card_num, exp_month, exp_year, cvc):
    resp = stripe.PaymentMethod.create(
        type="card",
        card={"number": f"{card_num}", "exp_month": f"{exp_month}",
              "exp_year": f"{exp_year}", "cvc": f"{cvc}"})
    pm_id = resp["id"]
    resp = stripe.PaymentMethod.attach(pm_id, customer=customer_id)
    return resp


def charge_card(amount, card_id, userid):
    # user id is the string provided by stripe to identify users
    try:
        intent = stripe.Charge.create(amount=amount, currency="usd",
                                      source="card_id", customer=userid)
    except stripe.error.CardError as e:
        return e.err
    # now backend can charge the card
    print(intent)
    return intent


def get_card_options(userid):
    query = f"SELECT stripe_id FROM stripe WHERE id = \'{userid}\'"
    data = inter.execute_read_query(query)
    if data:
        customer_id = data[0][0]
        customer = stripe.Customer.retrieve(f"{customer_id}")
        return customer["sources"]
