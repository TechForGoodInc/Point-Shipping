import interface as inter

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  username TEXT NOT NULL,
  id INTEGER,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT NOT NULL,
  addr VARCHAR,
  pswd VARCHAR
)
"""

create_label_table = """
CREATE TABLE IF NOT EXISTS labels (
    userid INTEGER,
    destination_address VARCHAR,
    sender_address VARCHAR,
    send_date DATE,
    price FLOAT,
    carrier VARCHAR
)
"""

#print(inter.execute_query("DROP TABLE users"))
print(inter.execute_query(create_users_table))
print(inter.execute_query(create_label_table))

