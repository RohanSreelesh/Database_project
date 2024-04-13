import os
import json
import psycopg2

# Database connection details
db_host = "localhost"
db_port = "5432"
db_name = "3005_v9"
db_user = "postgres"
db_password = "Rohan2002"

# Establish a connection to the database
conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cursor = conn.cursor()

# Directory containing the match files
match_files_directory = "../matches_curated/all"

# Iterate over the match files in the directory
for filename in os.listdir(match_files_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(match_files_directory, filename)
        
        # Read the JSON data from the file
        with open(file_path, encoding='utf-8') as file:
            matches = json.load(file)
        for match_data in matches:
            # print(match_data)
            # print("---------------------------------------------------")
            # print("---------------------------------------------------")
            # # Insert data into the competitions table
            competition_id = match_data['competition']['competition_id']
            season_id = match_data['season']['season_id']
            country_name = match_data['competition']['country_name']
            competition_name = match_data['competition']['competition_name']
            # cursor.execute("""
            #     INSERT INTO competitions (competition_id, season_id, country_name, competition_name)
            #     VALUES (%s, %s, %s, %s)
            #     ON CONFLICT (competition_id, season_id) DO NOTHING
            # """, (competition_id, season_id, country_name, competition_name))
            
            # Insert data into the referees table
            if 'referee' in match_data:
                referee_id = match_data['referee']['id']
                referee_name = match_data['referee']['name']
                referee_country = match_data['referee']['country']['name']
                referee_country_id = match_data['referee']['country']['id']
                cursor.execute("""
                    INSERT INTO referees (referee_id, referee_name, referee_country)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (referee_id) DO NOTHING
                """, (referee_id, referee_name, referee_country))
            else:
                referee_id = None
            
            # Insert data into the stadiums table
            if 'stadium' in match_data:
                stadium_id = match_data['stadium']['id']
                stadium_name = match_data['stadium']['name']
                stadium_country = match_data['stadium']['country']['name']
                cursor.execute("""
                    INSERT INTO stadiums (stadium_id, stadium_name, country)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (stadium_id) DO NOTHING
                """, (stadium_id, stadium_name, stadium_country)) 
            else:
                stadium_id = None
            
            # Insert data into the managers table
            if "managers" in match_data['home_team']:
                home_manager = match_data['home_team']['managers'][0]
                
                home_manager_id = home_manager['id']
                home_manager_name = home_manager['name']
                home_manager_nickname = home_manager['nickname']
                home_manager_dob = home_manager['dob']
                home_manager_country = home_manager['country']['name']
                
                cursor.execute("""
                    INSERT INTO managers (manager_id, manager_name, manager_nickname, manager_dob, manager_country)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (manager_id) DO NOTHING
                """, (home_manager_id, home_manager_name, home_manager_nickname, home_manager_dob, home_manager_country))
            else:
                home_manager_id = None

            if "managers" in match_data['away_team']:
                away_manager = match_data['away_team']['managers'][0]
                
                away_manager_id = away_manager['id']
                away_manager_name = away_manager['name']
                away_manager_nickname = away_manager['nickname']
                away_manager_dob = away_manager['dob']
                away_manager_country = away_manager['country']['name']
                
                cursor.execute("""
                    INSERT INTO managers (manager_id, manager_name, manager_nickname, manager_dob, manager_country)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (manager_id) DO NOTHING
                """, (away_manager_id, away_manager_name, away_manager_nickname, away_manager_dob, away_manager_country))
            else:
                away_manager_id = None
        # Insert data into the teams table
            home_team_id = match_data['home_team']['home_team_id']
            home_team_name = match_data['home_team']['home_team_name']
            home_team_gender = match_data['home_team']['home_team_gender']
            home_team_group = match_data['home_team']['home_team_group']
            home_team_country = match_data['home_team']['country']['name']
            
            away_team_id = match_data['away_team']['away_team_id']
            away_team_name = match_data['away_team']['away_team_name']
            away_team_gender = match_data['away_team']['away_team_gender']
            away_team_group = match_data['away_team']['away_team_group']
            away_team_country = match_data['away_team']['country']['name']
            
            cursor.execute("""
                INSERT INTO teams (team_id, team_name, team_gender, team_group, country, manager_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (team_id) DO NOTHING
            """, (home_team_id, home_team_name, home_team_gender, home_team_group, home_team_country, home_manager_id))
            
            cursor.execute("""
                INSERT INTO teams (team_id, team_name, team_gender, team_group, country, manager_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (team_id) DO NOTHING
            """, (away_team_id, away_team_name, away_team_gender, away_team_group, away_team_country, away_manager_id))
            
            # Insert data into the competition_stages table
            competition_stage_id = match_data['competition_stage']['id']
            competition_stage_name = match_data['competition_stage']['name']
            cursor.execute("""
                INSERT INTO competition_stages (competition_stage_id, competition_stage_name)
                VALUES (%s, %s)
                ON CONFLICT (competition_stage_id) DO NOTHING
            """, (competition_stage_id, competition_stage_name))

            # Insert data into the matches table
            match_id = match_data['match_id']
            match_date = match_data['match_date']
            kick_off = match_data['kick_off']
            home_score = match_data['home_score']
            away_score = match_data['away_score']
            match_week = match_data['match_week']

            cursor.execute("""
                INSERT INTO matches (
                    match_id, match_date, kick_off, competition_id, season_id,
                    home_team_id, away_team_id, home_score, away_score, match_week,
                    competition_stage_id, stadium_id, referee_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (match_id) DO NOTHING
            """, (
                match_id, match_date, kick_off, competition_id, season_id,
                home_team_id, away_team_id, home_score, away_score, match_week,
                competition_stage_id, stadium_id, referee_id
            ))
            
            conn.commit()

cursor.close()
conn.close()