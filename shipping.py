import json
from urllib.request import Request, urlopen
import json

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer sand_uQXMIPKfuVmebaIyOFTkEO6ziXpC0W3Gswd/MUkV0Xo=',
  'User-Agent': 'Mozilla/5.0'
}


def create_shipment(userid, dest_name, dest_add1, dest_add2, dest_city,
                    dest_state, dest_zip, dest_country, dest_phone,
                    item_description, weight, height, width, length,
                    category, currency, customs_val):

    vals = """
  {
    "platform_name": "Amazon",
    "platform_order_number": "#1234",
    "destination_country_alpha2": "US",
    "destination_city": "New York",
    "destination_postal_code": "10022",
    "destination_state": "NY",
    "destination_name": "Aloha Chen",
    "destination_address_line_1": "300 Park Avenue",
    "destination_address_line_2": null,
    "destination_phone_number": "+1 234-567-890",
    "destination_email_address": "api-support@easyship.com",
    "items": [
      {
        "description": "Silk dress",
        "sku": "test",
        "actual_weight": 1.2,
        "height": 10,
        "width": 15,
        "length": 20,
        "category": "fashion",
        "declared_currency": "SGD",
        "declared_customs_value": 100
      }
    ]
  }
    """

    updated_vals = vals.encode('ascii')
    request = Request('https://api.easyship.com/shipment/v1/shipments',
                      data=updated_vals, headers=headers)
    response_body = urlopen(request).read()
    print(response_body)
    return 0
