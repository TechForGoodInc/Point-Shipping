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
