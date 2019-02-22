import requests
import os

def stadium_id(db, stadium_info):

    db.query("""SELECT * FROM football_fcstadium WHERE stadium_name = %s AND city = %s""",
            (stadium_info['stadium_name'], stadium_info['city']))
    find_stadium = db.cursor.fetchone()
    if find_stadium:
        return find_stadium[0]
    else:
        db.query("""INSERT INTO football_fcstadium (stadium_name, city, capacity, url_stadium) VALUES (%s, %s, %s, %s) RETURNING id;""",
                (stadium_info['stadium_name'], stadium_info['city'], stadium_info['capacity'], stadium_info['url_image_stadium']))
        db.save()
        return db.cursor.fetchone()[0]


def download_image(url):

    response = requests.get(url)
    name_image = url.split('/')[-1]

    try:
        num_image = name_image.split('.')[0]
    except ValueError:
        num_image = 0
        return num_image

    if response.status_code == 200:
        if name_image not in os.listdir('../media/fc_logo'):
            with open(os.path.abspath('../media/fc_logo/{}'.format(name_image)), 'wb') as img:
                img.write(response.content)

    else:
        num_image = 0
    return num_image


def select_fc(db, fc_info, country_id, num_image, team_id):
    db.query(
        """SELECT * FROM football_footballclub WHERE fc_en_name = %s AND email = %s AND address = %s AND country_id = %s AND num_image = %s AND fc_id_name_dictionary_id = %s;""",
        (fc_info['fc_en_name'], fc_info['email'], fc_info['address'], country_id, num_image, team_id))

    find_fc = db.cursor.fetchone()
    if find_fc:
        return True
    else:
        return False


def save(db, dct_info, country_id, team_id):

    id_stadium = stadium_id(db, dct_info['stadium'])
    num_img = 0

    if dct_info['fc_logo']:
        print('logo = ', dct_info['fc_logo'])
        num_img = download_image(dct_info['fc_logo'])

    if not select_fc(db, dct_info, country_id, num_img, team_id):
        db.query(
            """INSERT INTO football_footballclub (fc_en_name, email, fax, address, phone, site, stadium_id, country_id, num_image, fc_id_name_dictionary_id, year_of_foundation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s);""",
            (dct_info['fc_en_name'], dct_info['email'], dct_info['fax'], dct_info['address'], dct_info['phone'], dct_info['official_site'], id_stadium, country_id, num_img, team_id, dct_info['foundation']))

        db.save()
    return

