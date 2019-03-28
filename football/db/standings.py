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
                CONSTRAINT unique_{name} UNIQUE (team_id, team_name, playedGames));""".format(name=name)
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
        # self.close()
        return result

    def update_team(self, table_name, team_info):
        # sel_team = self.select_team(table_name, team_info)
        # if sel_team is None:
        self.insert_team(table_name, team_info)
        # else:
        #     upd = """
        #     UPDATE
        #     """

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
        ) ON CONFLICT (team_id, team_name, playedGames) DO UPDATE SET
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
