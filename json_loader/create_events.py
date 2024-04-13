import os
import json
import psycopg2
import uuid

db_host = "localhost"
db_port = "5432"
db_name = "3005_v9"
db_user = "postgres"
db_password = "Rohan2002"
# Establish a connection to the database
conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cursor = conn.cursor()


# Directory containing the JSON files
json_directory = "../events_curated/all"


# Iterate over the JSON files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        print("Processing file:", filename)
        file_path = os.path.join(json_directory, filename)
        
        # Extract the match ID from the file name
        match_id = os.path.splitext(filename)[0]
        
        # Load the JSON data
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        
        # Iterate over the events data
        for event in data:
            event_id = event['id']
            event_index = event['index']
            period = event['period']
            timestamp = event['timestamp']
            minute = event['minute']
            second = event['second']
            type_id = event['type']['id']
            possession = event['possession']
            possession_team_id = event['possession_team']['id']
            play_pattern_id = event['play_pattern']['id']
            team_id = event['team']['id']
            team_name = event['team']['name']
            duration = event.get('duration')  
            
            # Insert event type data into the event_types table
            cursor.execute("INSERT INTO event_types (type_id, type_name) VALUES (%s, %s) ON CONFLICT (type_id) DO NOTHING", (type_id, event['type']['name']))
            
            # Insert play pattern data into the play_patterns table
            cursor.execute("INSERT INTO play_patterns (play_pattern_id, play_pattern_name) VALUES (%s, %s) ON CONFLICT (play_pattern_id) DO NOTHING", (play_pattern_id, event['play_pattern']['name']))
            
            # Insert event data into the events table
            cursor.execute("INSERT INTO events (event_id, match_id, event_index, period, timestamp, minute, second, type_id, possession, possession_team_id, play_pattern_id, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, event_index, period, timestamp, minute, second, type_id, possession, possession_team_id, play_pattern_id, duration))
            
            # Check if the event is a 50/50 event
            if event['type']['name'] == '50/50':
                player_id = event.get('player', {}).get('id') 
                position_id = event.get('position', {}).get('id')  
                location = event.get('location')  
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')  
                outcome_id = event.get('50_50', {}).get('outcome', {}).get('id') 
                counterpress = event.get('counterpress') 
                out = event.get('out') 
                
                # Insert outcome data into the outcomes table
                if '50_50' in event and 'outcome' in event['50_50']:
                    outcome_id = event['50_50']['outcome']['id']
                    outcome_name = event['50_50']['outcome']['name']
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))
                
                # Insert 50/50 event data into the the5050 table
                cursor.execute("INSERT INTO the5050 (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, outcome_id, counterpress, out, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, outcome_id, counterpress, out, team_id))

            if event['type']['name'] == 'Ball Receipt*':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                
                # Check if the 'ball_receipt' key exists and contains an 'outcome' key
                if 'ball_receipt' in event and 'outcome' in event['ball_receipt']:
                    outcome_id = event['ball_receipt']['outcome'].get('id')
                    outcome_name = event['ball_receipt']['outcome'].get('name')
                    
                    # Insert outcome data into the outcomes table
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))
                else:
                    outcome_id = None
                
                # Insert Ball Receipt event data into the BallReceipt table
                cursor.execute("INSERT INTO ballreceipt (event_id, match_id, player_id, position_id, location_x, location_y, outcome_id, under_pressure, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, outcome_id, under_pressure, team_id))

            if event['type']['name'] == 'Ball Recovery':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                out = event.get('out')
                recovery_failure = event.get('ball_recovery', {}).get('recovery_failure')
                offensive = event.get('ball_recovery', {}).get('offensive')
                off_camera = event.get('off_camera')

                # Insert Ball Recovery event data into the BallRecovery table
                cursor.execute("INSERT INTO BallRecovery (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, out, recovery_failure, offensive, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, out, recovery_failure, offensive, off_camera, team_id))

            if event['type']['name'] == 'Dispossessed':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                duration = event.get('duration')
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')

                # Insert Dispossessed event data into the Dispossessed table
                cursor.execute("INSERT INTO Dispossessed (event_id, match_id, player_id, position_id, location_x, location_y, duration, under_pressure, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, duration, under_pressure, off_camera, team_id))

            if event['type']['name'] == 'Duel':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                duel_type_name = event.get('duel', {}).get('type', {}).get('name')
                outcome_id = event.get('duel', {}).get('outcome', {}).get('id')
                counterpress = event.get('counterpress')
                off_camera = event.get('off_camera')

                # Insert outcome data into the outcomes table if it exists
                if outcome_id:
                    outcome_type_name = event.get('duel', {}).get('outcome', {}).get('name')
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_type_name))

                # Insert Duel event data into the Duel table
                cursor.execute("INSERT INTO Duel (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, duel_type_name, outcome_id, counterpress, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, duel_type_name, outcome_id, counterpress, off_camera, team_id))

            # Check if the event is a Block event
            if event['type']['name'] == 'Block':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                out = event.get('out')
                counterpress = event.get('counterpress')
                deflection = event.get('block', {}).get('deflection')
                offensive = event.get('block', {}).get('offensive')
                save_block = event.get('block', {}).get('save_block')
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')

                # Insert Block event data into the Block table
                cursor.execute("INSERT INTO Block (event_id, match_id, player_id, position_id, location_x, location_y, out, counterpress, deflection, offensive, save_block, under_pressure, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, out, counterpress, deflection, offensive, save_block, under_pressure, off_camera, team_id))


            if event['type']['name'] == 'Offside':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None

                # Insert Offside event data into the Offside table
                cursor.execute("INSERT INTO Offside (event_id, match_id, player_id, position_id, location_x, location_y, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, team_id))

            # Check if the event is a Clearance event
            if event['type']['name'] == 'Clearance':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                right_foot = event.get('clearance', {}).get('right_foot')
                body_part_name = event.get('clearance', {}).get('body_part', {}).get('name')
                left_foot = event.get('clearance', {}).get('left_foot')
                aerial_won = event.get('clearance', {}).get('aerial_won')
                head = event.get('clearance', {}).get('head')
                other = event.get('clearance', {}).get('other')
                out = event.get('out')
                off_camera = event.get('off_camera')

                # Insert Clearance event data into the Clearance table
                cursor.execute("INSERT INTO Clearance (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, right_foot, body_part_name, left_foot, aerial_won, head, other, out, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, right_foot, body_part_name, left_foot, aerial_won, head, other, out, off_camera, team_id))


            if event['type']['name'] == 'Interception':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                outcome_id = event.get('interception', {}).get('outcome', {}).get('id')
                counterpress = event.get('counterpress')
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')

                # Insert outcome data into the outcomes table if it exists
                if outcome_id:
                    outcome_name = event.get('interception', {}).get('outcome', {}).get('name')
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))

                # Insert Interception event data into the Interception table
                cursor.execute("INSERT INTO Interception (event_id, match_id, player_id, position_id, location_x, location_y, outcome_id, counterpress, under_pressure, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, outcome_id, counterpress, under_pressure, off_camera, team_id))

            # Check if the event is a Dribble event
            if event['type']['name'] == 'Dribble':
                player_id = event.get('player', {}).get('id')
                player_name = event.get('player', {}).get('name')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                duration = event.get('duration')
                under_pressure = event.get('under_pressure')
                outcome_id = event.get('dribble', {}).get('outcome', {}).get('id')
                outcome_name = event.get('dribble', {}).get('outcome', {}).get('name')
                overrun = event.get('dribble', {}).get('overrun')
                nutmeg = event.get('dribble', {}).get('nutmeg')
                no_touch = event.get('dribble', {}).get('no_touch')
                off_camera = event.get('off_camera')
                out = event.get('out')

                # Insert outcome data into the outcomes table if it exists
                if outcome_id:
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))

                # Insert Dribble event data into the Dribble table
                cursor.execute("INSERT INTO Dribble (event_id, match_id, player_id,player_name, position_id, location_x, location_y, duration, under_pressure, outcome_id, overrun, nutmeg, no_touch, off_camera, out, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id,player_name, position_id, location_x, location_y, duration, under_pressure, outcome_id, overrun, nutmeg, no_touch, off_camera, out, team_id))


            if event['type']['name'] == 'Shot':
                player_id = event.get('player', {}).get('id')
                player_name = event.get('player', {}).get('name')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                duration = event.get('duration')
                under_pressure = event.get('under_pressure')
                out = event.get('out')
                off_camera = event.get('off_camera')
                statsbomb_xg = event.get('shot', {}).get('statsbomb_xg')
                first_time = event.get('shot', {}).get('first_time')

                # Insert Shot event data into the Shot table
                cursor.execute("INSERT INTO Shot (event_id, match_id, player_id,player_name, position_id, location_x, location_y, duration, under_pressure, out, off_camera, statsbomb_xg, first_time, team_id, team_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id,player_name, position_id, location_x, location_y, duration, under_pressure, out, off_camera, statsbomb_xg, first_time, team_id,team_name))

                # Extract shot details
                end_location = event.get('shot', {}).get('end_location')
                if end_location:
                    end_location_x = end_location[0]
                    end_location_y = end_location[1]
                    if len(end_location) > 2:
                        end_location_z = end_location[2]
                    else:
                        end_location_z = 0
                else:
                    end_location_x = None
                    end_location_y = None
                key_pass_id = event.get('shot', {}).get('key_pass_id')
                body_part_name = event.get('shot', {}).get('body_part', {}).get('name')
                shot_type_name = event.get('shot', {}).get('type', {}).get('name')
                outcome_id = event.get('shot', {}).get('outcome', {}).get('id')
                outcome_name = event.get('shot', {}).get('outcome', {}).get('name')
                technique_name = event.get('shot', {}).get('technique', {}).get('name')
                deflected = event.get('shot', {}).get('deflected')
                one_on_one = event.get('shot', {}).get('one_on_one')
                aerial_won = event.get('shot', {}).get('aerial_won')
                saved_to_post = event.get('shot', {}).get('saved_to_post')
                redirect = event.get('shot', {}).get('redirect')
                open_goal = event.get('shot', {}).get('open_goal')
                follows_dribble = event.get('shot', {}).get('follows_dribble')
                saved_off_target = event.get('shot', {}).get('saved_off_target')

                # Insert outcome data into the outcomes table if it exists
                if outcome_id:
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))

                # Insert Shot_Details data into the Shot_Details table
                cursor.execute("INSERT INTO Shot_Details (event_id, end_location_x, end_location_y,end_location_z, key_pass_id, body_part_name, shot_type_name, outcome_id, technique_name, deflected, one_on_one, aerial_won, saved_to_post, redirect, open_goal, follows_dribble, saved_off_target) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, end_location_x, end_location_y,end_location_z, key_pass_id, body_part_name, shot_type_name, outcome_id, technique_name, deflected, one_on_one, aerial_won, saved_to_post, redirect, open_goal, follows_dribble, saved_off_target))

            # Check if the event is a Pressure event
            if event['type']['name'] == 'Pressure':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                counterpress = event.get('counterpress')
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')

                # Insert Pressure event data into the Pressure table
                cursor.execute("INSERT INTO Pressure (event_id, match_id, player_id, position_id, location_x, location_y, counterpress, under_pressure, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, counterpress, under_pressure, off_camera, team_id))

            # Check if the event is a Half Start event
            if event['type']['name'] == 'Half Start':
                late_video_start = event.get('late_video_start')

                # Insert Half Start event data into the HalfStart table
                cursor.execute("INSERT INTO HalfStart (event_id, late_video_start, team_id) VALUES (%s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, late_video_start, team_id))

            # Check if the event is a Substitution event
            if event['type']['name'] == 'Substitution':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                outcome_id = event.get('substitution', {}).get('outcome', {}).get('id')
                outcome_name = event.get('substitution', {}).get('outcome', {}).get('name')
                replacement_id = event.get('substitution', {}).get('replacement', {}).get('id')
                off_camera = event.get('off_camera')

                # Insert outcome data into the outcomes table if it exists
                if outcome_id:
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))

                # Insert Substitution event data into the Substitution table
                cursor.execute("INSERT INTO Substitution (event_id, match_id, player_id, position_id, outcome_id, replacement_id, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, outcome_id, replacement_id, off_camera, team_id))

            # Check if the event is an Own Goal Against event
            if event['type']['name'] == 'Own Goal Against':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None

                # Insert Own Goal Against event data into the OwnGoalAgainst table
                cursor.execute("INSERT INTO OwnGoalAgainst (event_id, match_id, player_id, position_id, location_x, location_y, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, team_id))


            if event['type']['name'] == 'Foul Won':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                penalty = event.get('foul_won', {}).get('penalty')
                defensive = event.get('foul_won', {}).get('defensive')
                advantage = event.get('foul_won', {}).get('advantage')
                off_camera = event.get('off_camera')

                # Insert Foul Won event data into the FoulWon table
                cursor.execute("INSERT INTO FoulWon (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, penalty, defensive, advantage, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, penalty, defensive, advantage, off_camera, team_id))

            # Check if the event is a Foul Committed event
            if event['type']['name'] == 'Foul Committed':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                counterpress = event.get('counterpress')
                penalty = event.get('foul_committed', {}).get('penalty')
                advantage = event.get('foul_committed', {}).get('advantage')
                card_name = event.get('foul_committed', {}).get('card', {}).get('name')
                offensive = event.get('foul_committed', {}).get('offensive')
                off_camera = event.get('off_camera')
                under_pressure = event.get('under_pressure')

                # Insert Foul Committed event data into the FoulCommitted table
                cursor.execute("INSERT INTO FoulCommitted (event_id, match_id, player_id, position_id, location_x, location_y, counterpress, penalty, advantage, card_name, offensive, off_camera, under_pressure, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, counterpress, penalty, advantage, card_name, offensive, off_camera, under_pressure, team_id))


            # Check if the event is a Goal Keeper event
            if event['type']['name'] == 'Goal Keeper':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                outcome_id = event.get('goalkeeper', {}).get('outcome', {}).get('id')
                outcome_name = event.get('goalkeeper', {}).get('outcome', {}).get('name')
                technique_name = event.get('goalkeeper', {}).get('technique', {}).get('name')
                goalkeeper_position_name = event.get('goalkeeper', {}).get('position', {}).get('name')
                body_part_name = event.get('goalkeeper', {}).get('body_part', {}).get('name')
                goalkeeper_type_name = event.get('goalkeeper', {}).get('type', {}).get('name')
                end_location = event.get('goalkeeper', {}).get('end_location')
                if end_location:
                    end_location_x = end_location[0]
                    end_location_y = end_location[1]
                else:
                    end_location_x = None
                    end_location_y = None
                shot_saved_to_post = event.get('goalkeeper', {}).get('shot_saved_to_post')
                punched_out = event.get('goalkeeper', {}).get('punched_out')
                success_in_play = event.get('goalkeeper', {}).get('success_in_play')
                shot_saved_off_target = event.get('goalkeeper', {}).get('shot_saved_off_target')
                lost_out = event.get('goalkeeper', {}).get('lost_out')
                lost_in_play = event.get('goalkeeper', {}).get('lost_in_play')
                out = event.get('out')
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')

                # Insert outcome data into the outcomes table if it exists
                if outcome_id:
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))

                # Insert Goal Keeper event data into the GoalKeeper table
                cursor.execute("INSERT INTO GoalKeeper (event_id, match_id, player_id, position_id, location_x, location_y, outcome_id, technique_name, goalkeeper_position_name, body_part_name, goalkeeper_type_name, end_location_x, end_location_y, shot_saved_to_post, punched_out, success_in_play, shot_saved_off_target, lost_out, lost_in_play, out, under_pressure, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, outcome_id, technique_name, goalkeeper_position_name, body_part_name, goalkeeper_type_name, end_location_x, end_location_y, shot_saved_to_post, punched_out, success_in_play, shot_saved_off_target, lost_out, lost_in_play, out, under_pressure, off_camera, team_id))

            if event['type']['name'] == 'Bad Behaviour':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                
                # Set position_id to None if it is 0
                if position_id == 0:
                    position_id = None
                
                card_name = event.get('bad_behaviour', {}).get('card', {}).get('name')
                off_camera = event.get('off_camera')
                
                # Insert Bad Behavior event data into the BadBehavior table
                cursor.execute("INSERT INTO BadBehavior (event_id, match_id, player_id, position_id, card_name, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, card_name, off_camera, team_id))

            # Check if the event is an Own Goal For event
            if event['type']['name'] == 'Own Goal For':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None

                # Insert Own Goal For event data into the OwnGoalFor table
                cursor.execute("INSERT INTO OwnGoalFor (event_id, match_id, player_id, position_id, location_x, location_y, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, team_id))

            # Check if the event is a Player On event
            if event['type']['name'] == 'Player On':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                off_camera = event.get('off_camera')

                # Insert Player On event data into the PlayerOn table
                cursor.execute("INSERT INTO PlayerOn (event_id, match_id, player_id, position_id, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, off_camera, team_id))

            # Check if the event is a Player Off event
            if event['type']['name'] == 'Player Off':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                off_camera = event.get('off_camera')

                # Insert Player Off event data into the PlayerOff table
                cursor.execute("INSERT INTO PlayerOff (event_id, match_id, player_id, position_id, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, off_camera, team_id))

            # Check if the event is a Shield event
            if event['type']['name'] == 'Shield':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')

                # Insert Shield event data into the Shield table
                cursor.execute("INSERT INTO Shield (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, team_id))



            # Check if the event is a Pass event
            if event['type']['name'] == 'Pass':
                player_id = event.get('player', {}).get('id')
                player_name = event.get('player', {}).get('name')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')
                counterpass = event.get('counterpass')
                out = event.get('out')
                recipient = event.get('pass', {}).get('recipient', {}).get('id')
                recipient_name = event.get('pass', {}).get('recipient', {}).get('name')
                through_ball = event.get('pass', {}).get('through_ball')

                # Insert Pass event data into the Pass table
                cursor.execute("INSERT INTO Pass (event_id, match_id, player_id, player_name,position_id, location_x, location_y, under_pressure, off_camera, counterpass, out, recipient,recipient_name, through_ball, team_id, team_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id,player_name, position_id, location_x, location_y, under_pressure, off_camera, counterpass, out, recipient,recipient_name, through_ball, team_id, team_name))

                # Extract pass details
                length = event.get('pass', {}).get('length')
                angle = event.get('pass', {}).get('angle')
                height = event.get('pass', {}).get('height', {}).get('name')
                end_location = event.get('pass', {}).get('end_location')
                if end_location:
                    end_location_x = end_location[0]
                    end_location_y = end_location[1]
                else:
                    end_location_x = None
                    end_location_y = None
                body_part_name = event.get('pass', {}).get('body_part', {}).get('name')
                type_name = event.get('pass', {}).get('type', {}).get('name')
                outcome_id = event.get('pass', {}).get('outcome', {}).get('id')
                outcome_name = event.get('pass', {}).get('outcome', {}).get('name')
                aerial_won = event.get('pass', {}).get('aerial_won')
                assisted_shot_id = event.get('pass', {}).get('assisted_shot_id')
                shot_assist = event.get('pass', {}).get('shot_assist')
                switch = event.get('pass', {}).get('switch')
                cross = event.get('pass', {}).get('cross')
                deflected = event.get('pass', {}).get('deflected')
                inswinging = event.get('pass', {}).get('inswinging')
                technique = event.get('pass', {}).get('technique', {}).get('name')
                no_touch = event.get('pass', {}).get('no_touch')
                outswinging = event.get('pass', {}).get('outswinging')
                miscommunication = event.get('pass', {}).get('miscommunication')
                cut_back = event.get('pass', {}).get('cut_back')
                goal_assist = event.get('pass', {}).get('goal_assist')
                straight = event.get('pass', {}).get('straight')

                # Insert outcome data into the outcomes table if it exists
                if outcome_id:
                    cursor.execute("INSERT INTO outcomes (outcome_id, outcome_name) VALUES (%s, %s) ON CONFLICT (outcome_id) DO NOTHING", (outcome_id, outcome_name))

                # Insert Pass_details data into the Pass_details table
                cursor.execute("INSERT INTO Pass_details (event_id, length, angle, height, end_location_x, end_location_y, body_part_name, type_name, outcome_id, aerial_won, assisted_shot_id, shot_assist, switch, cross_bool, deflected, inswinging, technique, no_touch, outswinging, miscommunication, cut_back, goal_assist, straight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, length, angle, height, end_location_x, end_location_y, body_part_name, type_name, outcome_id, aerial_won, assisted_shot_id, shot_assist, switch, cross, deflected, inswinging, technique, no_touch, outswinging, miscommunication, cut_back, goal_assist, straight))



            # Check if the event is a Starting XI event
            if event['type']['name'] == 'Starting XI':
                formation = event.get('tactics', {}).get('formation')

                # Insert Starting XI event data into the StartingXI table
                cursor.execute("INSERT INTO StartingXI (event_id, formation, team_id) VALUES (%s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, formation, team_id))

            # Check if the event is a Tactical Shift event
            if event['type']['name'] == 'Tactical Shift':
                formation = event.get('tactics', {}).get('formation')

                # Insert Tactical Shift event data into the TacticalShift table
                cursor.execute("INSERT INTO TacticalShift (event_id, formation, team_id) VALUES (%s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, formation,team_id))

            # Check if the event is a Dribbled Past event
            if event['type']['name'] == 'Dribbled Past':
                player_id = event.get('player', {}).get('id')
                player_name = event.get('player', {}).get('name')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                counterpress = event.get('counterpress')
                off_camera = event.get('off_camera')

                # Insert Dribbled Past event data into the DribbledPast table
                cursor.execute("INSERT INTO DribbledPast (event_id, match_id, player_id,player_name, position_id, location_x, location_y, counterpress, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id,player_name, position_id, location_x, location_y, counterpress, off_camera, team_id))

            # Check if the event is a Carry event
            if event['type']['name'] == 'Carry':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                end_location = event.get('carry', {}).get('end_location')
                if end_location:
                    end_location_x = end_location[0]
                    end_location_y = end_location[1]
                else:
                    end_location_x = None
                    end_location_y = None

                # Insert Carry event data into the Carry table
                cursor.execute("INSERT INTO Carry (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, end_location_x, end_location_y, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, end_location_x, end_location_y, team_id))

            # Check if the event is an Error event
            if event['type']['name'] == 'Error':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')

                # Insert Error event data into the Error table
                cursor.execute("INSERT INTO Error (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, under_pressure, off_camera, team_id))

            # Check if the event is an Injury Stoppage event
            if event['type']['name'] == 'Injury Stoppage':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                in_chain = event.get('injury_stoppage', {}).get('in_chain')
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')

                # Insert Injury Stoppage event data into the InjuryStoppage table
                cursor.execute("INSERT INTO InjuryStoppage (event_id, match_id, player_id, position_id, location_x, location_y, in_chain, under_pressure, off_camera, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, in_chain, under_pressure, off_camera, team_id))



            # Check if the event is a Miscontrol event
            if event['type']['name'] == 'Miscontrol':
                player_id = event.get('player', {}).get('id')
                position_id = event.get('position', {}).get('id')
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                in_chain = event.get('in_chain')
                under_pressure = event.get('under_pressure')
                off_camera = event.get('off_camera')
                out = event.get('out')
                aerial_won = event.get('miscontrol', {}).get('aerial_won')

                # Insert Miscontrol event data into the Miscontrol table
                cursor.execute("INSERT INTO Miscontrol (event_id, match_id, player_id, position_id, location_x, location_y, in_chain, under_pressure, off_camera, out, aerial_won, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, match_id, player_id, position_id, location_x, location_y, in_chain, under_pressure, off_camera, out, aerial_won, team_id))
            # Check if the event is a Referee Ball-Drop event
            if event['type']['name'] == 'Referee Ball-Drop':
                location = event.get('location')
                if location:
                    location_x = location[0]
                    location_y = location[1]
                else:
                    location_x = None
                    location_y = None
                off_camera = event.get('off_camera')

                # Insert Referee Ball-Drop event data into the RefereeBallDrop table
                cursor.execute("INSERT INTO RefereeBallDrop (event_id, location_x, location_y, off_camera, team_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (event_id) DO NOTHING", (event_id, location_x, location_y, off_camera, team_id))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
