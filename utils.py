import sqlite3


def open_database(sql_query):
    """
    Open database
    :param sql_query:
    :return: data by sql_query
    """
    try:
        with sqlite3.connect('./netflix.db') as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            data = cursor.fetchall()
        return data
    except sqlite3.Error:
        print('Loading data from database failed')


def search_by_title(user_title):
    """
    Function to search movie by title
    :param user_title:
    :return: list[dict] with movie by title
    """
    list_dict = []
    sql_query = (f"""
            SELECT `title`, `country`, `release_year`, `listed_in`, `description`
            FROM netflix
            WHERE `title` LIKE '%{user_title}%' AND type = 'Movie'
            ORDER BY `release_year` DESC
            LIMIT 1  
    """)
    data = open_database(sql_query)
    try:
        dict_ = {
            'title': data[0][0],
            'country': data[0][1],
            'release_year': data[0][2],
            'genre': data[0][3],
            'description': data[0][4].rstrip(),
        }
        list_dict.append(dict_)
        return list_dict
    except IndexError:
        return None


def search_by_year_range(year1, year2):
    """
    Function to search movies between year 1 and year 2
    :param year1:
    :param year2:
    :return: list[dict] with movies between year 1 and year 2
    """
    list_films = []
    sql_query = (f"""
            SELECT `title`, `release_year`
            FROM netflix
            WHERE `release_year` BETWEEN {year1} AND {year2}
            LIMIT 10
    """)
    data = open_database(sql_query)

    for row in data:
        dict_ = {
            'title': row[0],
            'release_year': row[1],
        }
        list_films.append(dict_)

    return list_films


def search_by_rating(film_rating):
    """
    Function to search movies by rating
    :param film_rating:
    :return: List[dict] with movies by rating
    """
    films_list = []
    dict_rating = {
        'children': '("G")',
        'adult': '("NC-17", "R")',
        'family': '("PG", "PG-13", "G")'
    }
    sql_query = (f"""
            SELECT `title`, `rating`, `description`
            From netflix
            WHERE `rating` IN {dict_rating[film_rating]}
    """)
    data = open_database(sql_query)

    for row in data:
        film = {
            'title': row[0],
            'rating': row[1],
            'description': row[2].rstrip()
        }
        films_list.append(film)

    return films_list


def search_by_genre(genre):
    """
    Function to search movies by genre
    :param genre:
    :return: list[dict] with movies by genre
    """
    list_dict = []
    sql_query = (f"""
            SELECT `title`, `description`
            FROM netflix
            WHERE `listed_in` LIKE '%{genre}%'
            ORDER BY `release_year` DESC
            LIMIT 10
    """)
    data = open_database(sql_query)

    for row in data:
        dict_ = {
            'title': row[0],
            'description': row[1].rstrip()
        }
        list_dict.append(dict_)

    return list_dict


def search_partners_coincidence(actor_1, actor_2):
    """
    Function to search partners, who played with actor_1 and actor_2 more than 2 times
    :param actor_1:
    :param actor_2:
    :return: list of actors who played with actor_1 and actor_2 more than 2 times
    """
    coincidence_list = []
    return_list = []
    sql_query = (f"""
        SELECT `cast`
        FROM netflix
        WHERE `cast` LIKE '%{actor_1}%' AND `cast` LIKE '%{actor_2}%'
    """)
    data = open_database(sql_query)

    for row in data:
        coincidence_list.extend(row[0].split(', '))
        for actor in coincidence_list:
            if actor == actor_1 or actor == actor_2:
                coincidence_list.remove(actor)

    for actor in coincidence_list:
        if coincidence_list.count(actor) > 2:
            if actor not in return_list:
                return_list.append(actor)
    return return_list


def search_by_type_release_year_genre(user_type, user_release, user_genre):
    """
    Function to search all movies by type, release_year and genre
    :param user_type:
    :param user_release:
    :param user_genre:
    :return: list of movies by type, release_year and genre
    """
    list_films = []
    sql_query = (f"""
        SELECT `title`, `description`
        FROM netflix
        WHERE `type` LIKE '%{user_type}%' AND `release_year` = {user_release} AND `listed_in` LIKE '%{user_genre}%'
    """)
    data = open_database(sql_query)

    for row in data:
        dict_ = {
            'title': row[0],
            'description': row[1].rstrip(),
        }
        list_films.append(dict_)
    return list_films
