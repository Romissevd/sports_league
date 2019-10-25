from parser.db import FCDataBase


class Standings(FCDataBase):

    def create_table(self, name):
        table = """CREATE TABLE IF NOT EXISTS football_{name} (
                id SERIAL NOT NULL PRIMARY KEY, 
                team_id INTEGER REFERENCES football_footballclub,
                team_name CHAR(200) NOT NULL,
                playedGames INTEGER NOT NULL, 
                points INTEGER NOT NULL, 
                goalsFor INTEGER NOT NULL, 
                goalsAgainst INTEGER NOT NULL,
                goalDifference INTEGER NOT NULL,
                won INTEGER NOT NULL, 
                draw INTEGER NOT NULL,
                lost INTEGER NOT NULL,
                CONSTRAINT unique_{name} UNIQUE (team_name));""".format(name=name)
        self.query(table)
        self.save()
        self.close()


    def select_team(self, table_name, data):
        search_team = """
        SELECT id FROM football_{table_name} WHERE team_id = %(id_team)s OR team_name = %(team_name)s;
        """.format(table_name=table_name)
        self.query(search_team, {'id_team': data['id_team'], 'team_name': data['team']['name']})
        result = None
        for item in self.cursor:
            result = item
        self.close()
        return result


    def insert_team(self, table_name, team_info):
        ins = """
        INSERT INTO football_{table_name} (
            team_id, 
            team_name, 
            playedGames, 
            points, 
            goalsFor, 
            goalsAgainst, 
            goalDifference, 
            won, 
            draw, 
            lost
        ) 
        VALUES (
            %(id_team)s, 
            %(team_name)s, 
            %(playedGames)s, 
            %(points)s,
            %(goalsFor)s, 
            %(goalsAgainst)s, 
            %(goalDifference)s, 
            %(won)s, 
            %(draw)s, 
            %(lost)s
        ) ON CONFLICT (team_name) DO UPDATE SET
            team_id = EXCLUDED.team_id,
            playedGames = EXCLUDED.playedGames, 
            points = EXCLUDED.points, 
            goalsFor = EXCLUDED.points, 
            goalsAgainst = EXCLUDED.goalsAgainst, 
            goalDifference = EXCLUDED.goalDifference, 
            won = EXCLUDED.won , 
            draw = EXCLUDED.draw, 
            lost = EXCLUDED.lost;
        """.format(table_name=table_name)
        self.query(ins, team_info)
        self.save()
        self.close()


class DBChampionsLeagueGS(FCDataBase):


    def select_team(self, table_name, data):
        search_team = """
        SELECT id FROM football_{table_name} WHERE team_id = %(id_team)s OR team_name = %(team_name)s;
        """.format(table_name=table_name)
        self.query(search_team, {'id_team': data['id_team'], 'team_name': data['team']['name']})
        result = None
        for item in self.cursor:
            result = item
        self.close()
        return result


    def insert_team(self, team_info):
        ins = """
        UPDATE football_championsleaguegroupstage SET 
            groups = %(groups)s,
            position = %(position)s,
            points = %(points)s,
            played_games = %(playedGames)s, 
            won = %(won)s, 
            draw = %(draw)s, 
            lost = %(lost)s,
            goals_difference = %(goalDifference)s,
            goals_against = %(goalsAgainst)s,
            goals_for = %(goalsFor)s, 
            last_update = %(lastUPD)s
            WHERE team_id = %(team_id)s AND start_year = %(start_year)s;
            INSERT INTO football_championsleaguegroupstage (
            team_id,
            groups,
            position, 
            points,
            played_games, 
            won, 
            draw, 
            lost,
            goals_difference, 
            goals_against,
            goals_for,
            start_year,
            end_year,
            last_update 
        ) 
        SELECT 
            %(team_id)s, 
            %(groups)s,
            %(position)s,
            %(points)s,  
            %(playedGames)s,
            %(won)s, 
            %(draw)s, 
            %(lost)s, 
            %(goalDifference)s, 
            %(goalsAgainst)s, 
            %(goalsFor)s, 
            %(start_year)s,
            %(end_year)s,
            %(lastUPD)s 
         
            WHERE NOT EXISTS (SELECT 1 FROM football_championsleaguegroupstage WHERE team_id = %(team_id)s AND start_year = %(start_year)s);
        """
        self.query(ins, team_info)
        self.save()
        self.close()


class DBChampionsLeagueMatches(FCDataBase):


    def insert_team(self, match_info):
        ins = """
        UPDATE football_championsleaguematches SET 
            groups = %(groups)s,
            stage = %(stage)s,
            status = %(status)s,
            time_match = %(time_match)s,
            away_team_extratime = %(away_team_extratime)s,
            home_team_extratime = %(home_team_extratime)s,
            away_team_fulltime = %(away_team_fulltime)s,
            home_team_fulltime = %(home_team_fulltime)s,
            away_team_halftime = %(away_team_halftime)s,
            home_team_halftime = %(home_team_halftime)s,
            away_team_penalties = %(away_team_penalties)s,
            home_team_penalties = %(home_team_penalties)s,
            winner = %(winner)s,
            end_year = %(end_year)s,
            last_updated = %(last_updated)s
            WHERE home_team_id = %(home_team)s AND away_team_id = %(away_team)s AND start_year = %(start_year)s;
            INSERT INTO football_championsleaguematches (
            home_team_id,
            away_team_id,
            groups,
            stage,
            status,
            time_match,
            away_team_extratime,
            home_team_extratime,
            away_team_fulltime,
            home_team_fulltime,
            away_team_halftime,
            home_team_halftime,
            away_team_penalties,
            home_team_penalties,
            winner,
            start_year,
            end_year,
            last_updated 
        ) 
        SELECT 
            %(home_team)s,
            %(away_team)s,
            %(groups)s,
            %(stage)s,
            %(status)s,
            %(time_match)s,
            %(away_team_extratime)s,
            %(home_team_extratime)s,
            %(away_team_fulltime)s,
            %(home_team_fulltime)s,
            %(away_team_halftime)s,
            %(home_team_halftime)s,
            %(away_team_penalties)s,
            %(home_team_penalties)s,
            %(winner)s,
            %(start_year)s,
            %(end_year)s,
            %(last_updated)s

            WHERE NOT EXISTS (SELECT 1 FROM football_championsleaguematches WHERE home_team_id = %(home_team)s AND away_team_id = %(away_team)s AND start_year = %(start_year)s);
        """
        self.query(ins, match_info)
        self.save()
        self.close()
