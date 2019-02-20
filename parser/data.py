from .db import FCDataBase


def save_country(country):

    dbc = FCDataBase()
    dbc.query("""SELECT * FROM football_countryruname WHERE country_name = %s;""",
              (country,) )
    if dbc.cursor.fetchall():
        print('Есть такая страна')
        return

    else:
        dbc.query("""INSERT INTO football_countryruname (country_name) VALUES (%s);""",
                  (country, ))
        dbc.save()
        print("added country")
    dbc.close()
