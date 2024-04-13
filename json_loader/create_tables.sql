
-- create competitions table

CREATE TABLE IF NOT EXISTS competitions (
        competition_id INTEGER,
        season_id INTEGER,
        country_name VARCHAR(255),
        competition_name VARCHAR(255),
        competition_gender VARCHAR(255),
        competition_youth BOOLEAN,
        competition_international BOOLEAN,
        season_name VARCHAR(255),
        PRIMARY KEY (competition_id, season_id)
    );


-- Create the referees table
CREATE TABLE referees (
    referee_id INTEGER PRIMARY KEY,
    referee_country_id INTEGER,
    referee_name VARCHAR(255),
    referee_country VARCHAR(255)
);

-- Create the stadiums table
CREATE TABLE stadiums (
    stadium_id INTEGER PRIMARY KEY,
    stadium_name VARCHAR(255),
    country VARCHAR(255)
);

-- Create the managers table
CREATE TABLE managers (
    manager_id INTEGER PRIMARY KEY,
    manager_name VARCHAR(255),
    manager_nickname VARCHAR(255),
    manager_dob DATE,
    manager_country VARCHAR(255)
);

-- Create the teams table
CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(255),
    team_gender VARCHAR(255),
    team_group VARCHAR(255),
    country VARCHAR(255),
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES managers (manager_id)
);

CREATE TABLE competition_stages (
    competition_stage_id INTEGER PRIMARY KEY,
    competition_stage_name VARCHAR(255)
);

-- Create the matches table
CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    match_date DATE,
    kick_off TIME,
    competition_id INTEGER,
    season_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    match_week INTEGER,
    competition_stage_id INTEGER,
    stadium_id INTEGER,
    referee_id INTEGER,
    FOREIGN KEY (competition_id, season_id) REFERENCES competitions (competition_id, season_id),
    FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams (team_id),
    FOREIGN KEY (stadium_id) REFERENCES stadiums (stadium_id),
    FOREIGN KEY (referee_id) REFERENCES referees (referee_id),
    FOREIGN KEY (competition_stage_id) REFERENCES competition_stages (competition_stage_id)
);


-- Create the players table
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name VARCHAR(255),
    player_nickname VARCHAR(255),
    country VARCHAR(255)
);

-- Create the lineups table
CREATE TABLE lineups (
    match_id INTEGER PRIMARY KEY,
    home_team_id INTEGER,
    away_team_id INTEGER,
    FOREIGN KEY (match_id) REFERENCES matches (match_id),
    FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams (team_id)
);

-- Create the lineup_players table
CREATE TABLE lineup_players (
    match_id INTEGER,
    player_id INTEGER,
    jersey_number INTEGER,
    first_card VARCHAR(255),
    second_card VARCHAR(255),
    PRIMARY KEY (match_id, player_id),
    FOREIGN KEY (match_id) REFERENCES lineups (match_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
);

-- Create the position_names table
CREATE TABLE position_names (
    position_id INTEGER PRIMARY KEY,
    position_name VARCHAR(255)
);

-- Create the positions table
CREATE TABLE positions (
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    start_time VARCHAR(10),
    end_time VARCHAR(10),
    start_period INTEGER,
    end_period INTEGER,
    start_reason VARCHAR(255),
    end_reason VARCHAR(255),
    PRIMARY KEY (match_id, player_id, position_id),
    FOREIGN KEY (match_id, player_id) REFERENCES lineup_players (match_id, player_id),
    FOREIGN KEY (position_id) REFERENCES position_names (position_id)
);


-- Create the event_types table
CREATE TABLE event_types (
    type_id INTEGER PRIMARY KEY,
    type_name VARCHAR(255)
);

-- Create the play_patterns table
CREATE TABLE play_patterns (
    play_pattern_id INTEGER PRIMARY KEY,
    play_pattern_name VARCHAR(255)
);

-- Create the outcomes table
CREATE TABLE outcomes (
    outcome_id INTEGER PRIMARY KEY,
    outcome_name VARCHAR(255)
);

-- Create the events table
CREATE TABLE events (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    event_index INTEGER,
    period INTEGER,
    timestamp VARCHAR(20),
    minute INTEGER,
    second INTEGER,
    type_id INTEGER,
    possession INTEGER,
    possession_team_id INTEGER,
    play_pattern_id INTEGER,
    duration FLOAT,
    FOREIGN KEY (match_id) REFERENCES matches (match_id),
    FOREIGN KEY (type_id) REFERENCES event_types (type_id),
    FOREIGN KEY (possession_team_id) REFERENCES teams (team_id),
    FOREIGN KEY (play_pattern_id) REFERENCES play_patterns (play_pattern_id)
);

-- Create the the5050 table
CREATE TABLE the5050 (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    outcome_id INTEGER,
    counterpress BOOLEAN,
    out BOOLEAN,
    team_id INTEGER,    
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the BallReceipt table
CREATE TABLE BallReceipt (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    outcome_id INTEGER,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the BallRecovery table
CREATE TABLE BallRecovery (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    out BOOLEAN,
    recovery_failure BOOLEAN,
    offensive BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Dispossessed table
CREATE TABLE Dispossessed (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the Duel table
CREATE TABLE Duel (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    duel_type_name VARCHAR(255),
    duel_type_id INTEGER,
    outcome_id INTEGER,
    counterpress BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Block table
CREATE TABLE Block (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    out BOOLEAN,
    counterpress BOOLEAN,
    deflection BOOLEAN,
    offensive BOOLEAN,
    save_block BOOLEAN,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the Offside table
CREATE TABLE Offside (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Clearance table
CREATE TABLE Clearance (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    right_foot BOOLEAN,
    body_part_name VARCHAR(255),
    left_foot BOOLEAN,
    aerial_won BOOLEAN,
    head BOOLEAN,
    other BOOLEAN,
    out BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the Interception table
CREATE TABLE Interception (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    outcome_id INTEGER,
    counterpress BOOLEAN,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Dribble table
CREATE TABLE Dribble (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    player_name VARCHAR(255),
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    outcome_id INTEGER,
    overrun BOOLEAN,
    nutmeg BOOLEAN,
    no_touch BOOLEAN,
    off_camera BOOLEAN,
    out BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the Shot table
CREATE TABLE Shot (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    player_name VARCHAR(255),
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    duration FLOAT,
    under_pressure BOOLEAN,
    out BOOLEAN,
    off_camera BOOLEAN,
    statsbomb_xg FLOAT,
    first_time BOOLEAN,
    team_id INTEGER, 
    team_name VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Shot_Details table
CREATE TABLE Shot_Details (
    event_id UUID PRIMARY KEY,
    end_location_x FLOAT,
    end_location_y FLOAT,
    end_location_z FLOAT,
    key_pass_id UUID,
    body_part_name VARCHAR(255),
    shot_type_id INTEGER,
    shot_type_name VARCHAR(255),
    outcome_id INTEGER,
    technique_id INTEGER,
    technique_name VARCHAR(255),
    deflected BOOLEAN,
    one_on_one BOOLEAN,
    aerial_won BOOLEAN,
    saved_to_post BOOLEAN,
    redirect BOOLEAN,
    open_goal BOOLEAN,
    follows_dribble BOOLEAN,
    saved_off_target BOOLEAN,
    FOREIGN KEY (event_id) REFERENCES Shot (event_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id)
);


-- Create the Pressure table
CREATE TABLE Pressure (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    counterpress BOOLEAN,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the HalfStart table
CREATE TABLE HalfStart (
    event_id UUID PRIMARY KEY,
    late_video_start BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Substitution table
CREATE TABLE Substitution (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    outcome_id INTEGER,
    replacement_id INTEGER,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (replacement_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the OwnGoalAgainst table
CREATE TABLE OwnGoalAgainst (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the FoulWon table
CREATE TABLE FoulWon (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    penalty BOOLEAN,
    defensive BOOLEAN,
    advantage BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the FoulCommitted table
CREATE TABLE FoulCommitted (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    counterpress BOOLEAN,
    penalty BOOLEAN,
    advantage BOOLEAN,
    card_name VARCHAR(255),
    offensive BOOLEAN,
    off_camera BOOLEAN,
    under_pressure BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
	);

-- Create the GoalKeeper table
CREATE TABLE GoalKeeper (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    outcome_id INTEGER,
    technique_id INTEGER,
    technique_name VARCHAR(255),
    goalkeeper_position_id INTEGER,
    goalkeeper_position_name VARCHAR(255),
    body_part_name VARCHAR(255),
    goalkeeper_type_id INTEGER,
    goalkeeper_type_name VARCHAR(255),
    end_location_x FLOAT,
    end_location_y FLOAT,
    shot_saved_to_post BOOLEAN,
    punched_out BOOLEAN,
    success_in_play BOOLEAN,
    shot_saved_off_target BOOLEAN,
    lost_out BOOLEAN,
    lost_in_play BOOLEAN,
    out BOOLEAN,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the BadBehavior table
CREATE TABLE BadBehavior (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    card_name VARCHAR(255),
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the OwnGoalFor table
CREATE TABLE OwnGoalFor (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the PlayerOn table
CREATE TABLE PlayerOn (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the PlayerOff table
CREATE TABLE PlayerOff (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Shield table
CREATE TABLE Shield (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the Pass table
CREATE TABLE Pass (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    player_name VARCHAR(255),
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    counterpass BOOLEAN,
    out BOOLEAN,
    recipient INTEGER,
    recipient_name VARCHAR(255),
    through_ball BOOLEAN,
    team_id INTEGER, 
    team_name VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (recipient) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Pass_details table
CREATE TABLE Pass_details (
    event_id UUID PRIMARY KEY,
    length FLOAT,
    angle FLOAT,
    height VARCHAR(255),
    end_location_x FLOAT,
    end_location_y FLOAT,
    body_part_name VARCHAR(255),
    type_id INTEGER,
    type_name VARCHAR(255),
    outcome_id INTEGER,
    aerial_won BOOLEAN,
    assisted_shot_id UUID,
    shot_assist BOOLEAN,
    switch BOOLEAN,
    cross_bool BOOLEAN,
    deflected BOOLEAN,
    inswinging BOOLEAN,
    technique VARCHAR(255),
    no_touch BOOLEAN,
    outswinging BOOLEAN,
    miscommunication BOOLEAN,
    cut_back BOOLEAN,
    goal_assist BOOLEAN,
    straight BOOLEAN,
    FOREIGN KEY (event_id) REFERENCES Pass (event_id),
    FOREIGN KEY (outcome_id) REFERENCES outcomes (outcome_id)
);



-- Create the StartingXI table
CREATE TABLE StartingXI (
    event_id UUID PRIMARY KEY,
    formation INTEGER,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the TacticalShift table
CREATE TABLE TacticalShift (
    event_id UUID PRIMARY KEY,
    formation INTEGER,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the DribbledPast table
CREATE TABLE DribbledPast (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    player_name VARCHAR(255),
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    counterpress BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Carry table
CREATE TABLE Carry (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    end_location_x FLOAT,
    end_location_y FLOAT,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the Error table
CREATE TABLE Error (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the InjuryStoppage table
CREATE TABLE InjuryStoppage (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    in_chain BOOLEAN,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);


-- Create the Miscontrol table
CREATE TABLE Miscontrol (
    event_id UUID PRIMARY KEY,
    match_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,
    location_x FLOAT,
    location_y FLOAT,
    in_chain BOOLEAN,
    under_pressure BOOLEAN,
    off_camera BOOLEAN,
    out BOOLEAN,
    aerial_won BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (match_id, player_id, position_id) REFERENCES positions (match_id, player_id, position_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

-- Create the RefereeBallDrop table
CREATE TABLE RefereeBallDrop (
    event_id UUID PRIMARY KEY,
    location_x FLOAT,
    location_y FLOAT,
    off_camera BOOLEAN,
    team_id INTEGER, 
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);

CREATE INDEX idx_match_id ON matches(match_id);
CREATE INDEX idx_matches_on_ids ON matches (match_id, competition_id, season_id);
CREATE INDEX idx_competitions_on_name_season ON competitions (competition_name, season_name);
CREATE INDEX idx_shot_match_id ON Shot (match_id);
CREATE INDEX idx_pass_match_id ON Pass (match_id);
CREATE INDEX idx_dribble_match_id ON Dribble (match_id);