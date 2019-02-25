def country_id(db, country):

    db.query("""SELECT * FROM football_countryruname WHERE country_name = %s;""",
              (country,) )
    find_country = db.cursor.fetchone()
    if find_country:
        return find_country[0]

    else:
        db.query("""INSERT INTO football_countryruname (country_name) VALUES (%s) RETURNING id;""",
                  (country, ))
        db.save()
        return db.cursor.fetchone()[0]


def league_id(db, league):

    db.query("""SELECT * FROM football_league WHERE league_name = %s;""",
              (league,) )
    find_league = db.cursor.fetchone()
    if find_league:
        return find_league[0]

    else:
        db.query("""INSERT INTO football_league (league_name) VALUES (%s) RETURNING id;""",
                  (league, ))
        db.save()
        return db.cursor.fetchone()[0]


def club_name_id(db, club):
    db.query("""SELECT * FROM football_dictionaryclubname WHERE club_name = %s;""",
             (club,))
    find_club = db.cursor.fetchone()
    if find_club:
        return find_club[0]

    else:
        db.query("""INSERT INTO football_dictionaryclubname (club_name) VALUES (%s) RETURNING id;""",
                 (club,))
        db.save()
        return db.cursor.fetchone()[0]


def save_team(db, country, league, teams):

    id_country = country_id(db, country)
    id_league = league_id(db, league)

    for team in teams:
        name_team = team.text

        try:
            url_team = team.find_element_by_tag_name("a").get_attribute('href')
        except:
            url_team = ''

        id_team = club_name_id(db, name_team)

        db.query("""SELECT * FROM football_parsingdata WHERE country_id = %s AND league_id = %s AND name_id = %s;""",
                 (id_country, id_league, id_team))

        find_team = db.cursor.fetchone()
        if not find_team:
            db.query("""INSERT INTO football_parsingdata (link_for_parsing, country_id, league_id, name_id) VALUES (%s, %s, %s, %s) RETURNING id;""",
                     (url_team, id_country, id_league, id_team))
            db.save()
    return
