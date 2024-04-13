import psycopg2
import json

# Database connection 
db_host = "localhost"
db_port = "5432"
db_name = "3005_v9"
db_user = "postgres"
db_password = "Rohan2002"

# Establish a connection 
conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cursor = conn.cursor()
# Read the JSON data from file
with open('../competitions.json', encoding="utf-8") as file:
    competitions_data = json.load(file)

insert_query = """
    INSERT INTO competitions (
        competition_id, season_id, country_name, competition_name,
        competition_gender, competition_youth, competition_international,
        season_name
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# Iterate over the competitions data and insert each record
for competition in competitions_data:
    values = (
        competition['competition_id'],
        competition['season_id'],
        competition['country_name'],
        competition['competition_name'],
        competition['competition_gender'],
        competition['competition_youth'],
        competition['competition_international'],
        competition['season_name']
    )
    cursor.execute(insert_query, values)

conn.commit()