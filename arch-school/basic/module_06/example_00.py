import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://arch_user:arch_password@127.0.0.1:3360/archdb", echo = True)

df = pd.read_json("ExportJson.json")
df.to_sql("Author", con=engine, if_exists = 'replace', index=False)