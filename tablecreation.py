import interface as inter

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  username TEXT NOT NULL,
  id INTEGER,
  email TEXT NOT NULL,
  sender TEXT NOT NULL,
  street VARCHAR,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zip INTEGER,
  country TEXT NOT NULL,
  password VARCHAR
)
"""

create_label_table = """
CREATE TABLE IF NOT EXISTS labels (
  userid INTEGER,
  shipment VARCHAR,
  carrier VARCHAR
)
"""

print(inter.execute_query("DROP TABLE users"))
print(inter.execute_query("DROP TABLE labels"))
print(inter.execute_query(create_users_table))
print(inter.execute_query(create_label_table))

"""
vals = (
        {\"dest_name\": \"{dest_name}\", "
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
"""