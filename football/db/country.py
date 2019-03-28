from parser.db import FCDataBase


class Country(FCDataBase):

    def from_en_to_ru(self, name):
        country = """
            SELECT ru_name_id FROM football_countryenname WHERE country_name = %(name)s;
        """
        self.query(country, {'name': name})
        id = None
        for item in self.cursor:
            id = item[0]
        self.close()

        if id is None:
            print("Warning!!! Нет такой страны")

        return id


