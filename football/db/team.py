from parser.db import FCDataBase


class Team(FCDataBase):

    def search_team(self, name, country):
        club = """
            SELECT id FROM football_footballclub WHERE fc_en_name = %(name)s 
            AND country_id = %(country)s OR alt_name = %(name)s 
            AND country_id = %(country)s;
        """
        self.query(club, {'name': name, 'country': country})
        id = None
        for item in self.cursor:
            id = item[0]
        self.close()

        if id is None:
            print("Warning!!! Нет такой команды - {}".format(name))

        return id