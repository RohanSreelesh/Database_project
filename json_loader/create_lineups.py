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



json_directory = "../lineups_curated/all"

for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        
        # Extract the match ID from the file name
        match_id = os.path.splitext(filename)[0]
        
        # Load
        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)
        
        # Insert match ID into the lineups table
        home_team_id = data[0]['team_id']
        away_team_id = data[1]['team_id']
        cursor.execute("INSERT INTO lineups (match_id, home_team_id, away_team_id) VALUES (%s, %s, %s) ON CONFLICT (match_id) DO NOTHING", (match_id, home_team_id, away_team_id))
        
        # Iterate over the lineup data
        for team in data:
            team_id = team['team_id']
            team_name = team['team_name']
            
            # Insert team data into the teams table
            #cursor.execute("INSERT INTO teams (team_id, team_name) VALUES (%s, %s) ON CONFLICT (team_id) DO NOTHING", (team_id, team_name))
            
            for player in team['lineup']:
                player_id = player['player_id']
                player_name = player['player_name']
                player_nickname = player['player_nickname']
                country = player['country']['name']
                
                # Insert player data into the players table
                cursor.execute("INSERT INTO players (player_id, player_name, player_nickname, country) VALUES (%s, %s, %s, %s) ON CONFLICT (player_id) DO NOTHING", (player_id, player_name, player_nickname, country))
                
                jersey_number = player['jersey_number']
                
                # Check if the player has cards
                if 'cards' in player:
                    cards = player['cards']
                    if len(cards) > 0:
                        first_card = cards[0]['card_type']
                        if len(cards) > 1:
                            second_card = cards[1]['card_type']
                        else:
                            second_card = None
                    else:
                        first_card = None
                        second_card = None
                else:
                    first_card = None
                    second_card = None
                
                # Insert player data into the lineup_players table
                cursor.execute("INSERT INTO lineup_players (match_id, player_id, jersey_number, first_card, second_card) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (match_id, player_id) DO NOTHING", (match_id, player_id, jersey_number, first_card, second_card))
                
                # Process player positions
                for position in player['positions']:
                    position_id = position['position_id']
                    position_name = position['position']
                    
                    # Insert position data into the position_names table
                    cursor.execute("INSERT INTO position_names (position_id, position_name) VALUES (%s, %s) ON CONFLICT (position_id) DO NOTHING", (position_id, position_name))
                    
                    start_time = position['from']
                    end_time = position['to']
                    start_period = position['from_period']
                    end_period = position['to_period']
                    start_reason = position['start_reason']
                    end_reason = position['end_reason']
                    
                    # Insert position data into the positions table
                    cursor.execute("INSERT INTO positions (match_id, player_id, position_id, start_time, end_time, start_period, end_period, start_reason, end_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (match_id, player_id, position_id) DO NOTHING", (match_id, player_id, position_id, start_time, end_time, start_period, end_period, start_reason, end_reason))

# Commit
conn.commit()
cursor.close()
conn.close()