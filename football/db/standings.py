from parser.db import FCDataBase


class Standings(FCDataBase):

    def create_table(self):
        pass

    def search_table(self, name):
        table = """CREATE TABLE IF NOT EXISTS football_{name} (
                id INTEGER PRIMARY KEY, 
                team_id INTEGER REFERENCES football_footballclub, 
                playedGames INTEGER, 
                points INTEGER, 
                goalsFor INTEGER, 
                goalsAgainst INTEGER, 
                win INTEGER, 
                lost INTEGER, 
                draw INTEGER,
                );""".format(name=name)
        self.query(table)
        self.save()
        self.close()