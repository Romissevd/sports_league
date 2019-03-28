from parser.db import FCDataBase


class Standings(FCDataBase):

    def create_table(self, name):
        table = """CREATE TABLE IF NOT EXISTS football_{name} (
                id INTEGER PRIMARY KEY, 
                team_id INTEGER REFERENCES football_footballclub,
                team_name CHAR(200) NULL,
                playedGames INTEGER, 
                points INTEGER, 
                goalsFor INTEGER, 
                goalsAgainst INTEGER,
                goalDifference INTEGER,
                won INTEGER, 
                draw INTEGER,
                lost INTEGER
                );""".format(name=name)
        self.query(table)
        self.save()
        self.close()
