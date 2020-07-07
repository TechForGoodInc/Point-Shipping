import interface as inter

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  username TEXT NOT NULL,
  id INTEGER,
  email TEXT NOT NULL,
  ez_address_id VARCHAR,
  password VARCHAR
)
"""

create_label_table = """
CREATE TABLE IF NOT EXISTS labels (
  userid INTEGER,
  shipment VARCHAR,
  send_date DATE,
  carrier VARCHAR
)
"""

#create_photo_table = """
#CREATE TABLE IF NOT EXISTS photos (
#  pic VARBINARY(MAX),
#  userid INTEGER
#  )
#"""

#print(inter.execute_query("DROP TABLE users"))
#print(inter.execute_query("DROP TABLE labels"))
#print(inter.execute_query("DROP TABLE photos"))
print(inter.execute_query(create_users_table))
print(inter.execute_query(create_label_table))
#print(inter.execute_query(create_photo_table))

