import interface as inter

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  username TEXT NOT NULL,
  id INTEGER,
  email TEXT NOT NULL,
  ez_address_id VARCHAR,
  password VARBINARY(1024)
)
"""

create_label_table = """
CREATE TABLE IF NOT EXISTS labels (
  userid INTEGER,
  ez_address_sender VARCHAR,
  ez_address_reciever VARCHAR,

  length FLOAT,
  width FLOAT,
  height FLOAT,
  weight FLOAT,

  send_date DATE,
  price FLOAT,
  carrier VARCHAR
)
"""

print(inter.execute_query("DROP TABLE users"))
print(inter.execute_query("DROP TABLE labels"))
print(inter.execute_query(create_users_table))
print(inter.execute_query(create_label_table))

