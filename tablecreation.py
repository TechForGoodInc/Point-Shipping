import interface as inter

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  username TEXT NOT NULL,
  id INTEGER,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT NOT NULL,
  sender_name TEXT NOT NULL,
  sender_street VARCHAR,
  sender_city TEXT NOT NULL,
  sender_state TEXT NOT NULL,
  sender_zip INTEGER,
  sender_country TEXT NOT NULL,
  pswd VARCHAR
)
"""

create_label_table = """
CREATE TABLE IF NOT EXISTS labels (
  userid INTEGER,
  sender_name TEXT NOT NULL,
  sender_street VARCHAR,
  sender_city TEXT NOT NULL,
  sender_state TEXT NOT NULL,
  sender_zip INTEGER,
  sender_country TEXT NOT NULL,

  reciever_name TEXT NOT NULL,
  reciever_street VARCHAR,
  reciever_city TEXT NOT NULL,
  reciever_state TEXT NOT NULL,
  reciever_zip INTEGER,
  reciever_country TEXT NOT NULL,

  length FLOAT,
  width FLOAT,
  height FLOAT,
  weight FLOAT,

  send_date DATE,
  price FLOAT,
  carrier VARCHAR
)
"""

#print(inter.execute_query("DROP TABLE users"))
#print(inter.execute_query("DROP TABLE labels"))
print(inter.execute_query(create_users_table))
print(inter.execute_query(create_label_table))

