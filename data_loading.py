import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Initialize the Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# load dataset
df = pd.read_csv("cybersecurity_threat_detection_logs.csv")
df = df.head(10000)

# convert each record of the df into a dictionary object
# records will become a list of dictionaries
records = df.to_dict(orient="records")

# insert bulk data into supabase using api
response = (
    supabase.table("cybersecurity_threat_detection_logs").insert(records).execute()
)
