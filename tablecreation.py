import interface as inter

create_stripe_id_table = """
CREATE TABLE IF NOT EXISTS stripe (
  id INTEGER,
  stripe_id VARCHAR
)
"""

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
  platform TEXT NOT NULL,
  dest_name VARCHAR,
  dest_add1 TEXT NOT NULL,
  dest_add2 TEXT,
  dest_city TEXT NOT NULL,
  dest_state TEXT NOT NULL,
  dest_zip INTEGER,
  dest_country TEXT NOT NULL,
  dest_number VARCHAR,
  dest_email VARCHAR,
  pkg_length FLOAT,
  pkg_width FLOAT,
  pkg_height FLOAT,
  pkg_weight FLOAT,
  courierid VARCHAR
)
"""

print(inter.execute_query("DROP TABLE users"))
print(inter.execute_query("DROP TABLE labels"))
print(inter.execute_query("DROP TABLE stripe"))
print(inter.execute_query(create_users_table))
print(inter.execute_query(create_label_table))
print(inter.execute_query(create_stripe_id_table))
