from sqlalchemy import create_engine
import pandas as pd

URL = "postgresql://lector_user:password@db.eazsiksqqitvvkhjpxop.supabase.co:5432/postgres"

engine = create_engine(URL)
query = "SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'public'"
result = pd.read_sql_query(query, engine)

for lab, row in result.iterrows():
    table_name = row['table_name']
    query = f"SELECT * FROM {table_name}"
    result = pd.read_sql_query(query, engine)
    result.reset_index(drop=True, inplace=True)
    path = f"data/raw/{table_name}.csv"
    result.to_csv(path, index=False)