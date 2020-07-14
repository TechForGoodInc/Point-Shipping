import requests
import json
from urllib.request import Request, urlopen
import json

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer sand_uQXMIPKfuVmebaIyOFTkEO6ziXpC0W3Gswd/MUkV0Xo='
}


def create_shipment(userid, dest_name, dest_add1, dest_add2, dest_city,
                    dest_state, dest_zip, dest_country, dest_phone,
                    item_description, weight, height, width, length,
                    category, currency, customs_val):
    vals = (
        f"\u007b\"dest_name\": \"{dest_name}\", "
        f"\"destination_address_line_1\": \"{dest_add1}\","
        f"\"destination_address_line_2\": \"{dest_add2}\", "
        f"\"destination_city\": \"{dest_city}\", "
        f"\"destination_state\": \"{dest_state}\", "
        f"\"destination_postal_code\": {dest_zip}, "
        f"\"destination_country_alpha2\": \"{dest_country}\", "
        f"\"destination_phone_number\": \"{dest_phone}\", "
        f"\"items\": \u007b\"description\": \"{item_description}\", "
        f"\"sku\": \"test\", \"actual_weight\": {weight}, "
        f"\"height\": {height}, \"width\": {width}, "
        f"\"length\": {length}, \"category\": \"{category}\", "
        f"\"declared_currency\": \"{currency}\", "
        f"\"declared_customs_value\": {customs_val}\u007d\u007d"
    )
    print(type(vals))
    print("\n")
    print(vals)
    print("\n")
    package_vals = json.loads(vals)
    print("here2")
    request = Request('https://api.easyship.com/shipment/v1/shipments',
                      data=package_vals, headers=headers)

    response_body = urlopen(request).read()
    print(response_body)
    return 0
