import psycopg2


class FCDataBase():

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='sports_league',
            user='sportsman',
            password='sport',
            host='localhost',
            )
        self.cursor = self.conn.cursor()

    def query(self, query, args=None):
        self.cursor.execute(query, args)

    def save(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db = FCDataBase()
    db.query("""SELECT * FROM user_profile;""")
    for row in db.cursor:
        print(row)

    db.close()
