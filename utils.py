import sqlite3


class DatabaseDAO:

    def __init__(self, path):
        self.path = path

    def open_database(self, sql_query):
        """Open database"""
        list_ = []
        try:
            with sqlite3.connect(self.path) as connection:
                connection.row_factory = sqlite3.Row
                data = connection.execute(sql_query).fetchall()
                for item in data:
                    result = dict(item)
                    list_.append(result)
            return list_
        except sqlite3.Error:
            print('Loading data from database failed')

    def search_by_title(self, user_title):
        """Function to search movie by title"""
        sql_query = (f"""
                SELECT `title`, `country`, `release_year`, `listed_in`, `description`
                FROM netflix
                WHERE `title` LIKE '%{user_title}%'
                ORDER BY `release_year` DESC
                LIMIT 1  
        """)

        result = self.open_database(sql_query)
        return result

    def search_by_year_range(self, year1, year2):
        """Function to search movies between year 1 and year 2"""
        sql_query = (f"""
                SELECT `title`, `release_year`
                FROM netflix
                WHERE `release_year` BETWEEN {year1} AND {year2}
                LIMIT 10
        """)
        result = self.open_database(sql_query)
        return result

    def search_by_rating(self, film_rating):
        """Function to search movies by rating"""
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
        result = self.open_database(sql_query)
        return result

    def search_by_genre(self, genre):
        """Function to search movies by genre"""
        sql_query = (f"""
                SELECT `title`, `description`
                FROM netflix
                WHERE `listed_in` LIKE '%{genre}%'
                ORDER BY `release_year` DESC
                LIMIT 10
        """)
        result = self.open_database(sql_query)
        return result

    def search_partners_coincidence(self, actor_1, actor_2):
        """Function to search partners, who played with actor_1 and actor_2 more than 2 times"""
        coincidence_list = []
        return_list = []
        sql_query = (f"""
                SELECT `cast`
                FROM netflix
                WHERE `cast` LIKE '%{actor_1}%' AND `cast` LIKE '%{actor_2}%'
        """)
        data = self.open_database(sql_query)
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

    def search_by_type_release_year_genre(self, user_type, user_release, user_genre):
        """Function to search all movies by type, release_year and genre"""
        sql_query = (f"""
            SELECT `title`, `description`
            FROM netflix
            WHERE `type` LIKE '%{user_type}%' AND `release_year` = {user_release} AND `listed_in` LIKE '%{user_genre}%'
        """)
        result = self.open_database(sql_query)
        return result
