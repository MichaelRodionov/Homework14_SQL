from flask import Flask, jsonify
import utils as u

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/movie/<title>')
def view_by_title(title):
    """View returns movie, found by title"""
    list_films = u.search_by_title(title)
    return jsonify(list_films)


@app.route('/movie/<int:year1>/to/<int:year2>')
def view_by_year_to_year(year1, year2):
    """View returns movies found by year to year"""
    list_films = u.search_by_year_range(year1, year2)
    return jsonify(list_films)


@app.route('/rating/<rating>')
def view_by_rating(rating):
    """View returns movies, filtered by rating"""
    list_films = u.search_by_rating(rating)
    return jsonify(list_films)


@app.route('/genre/<genre>')
def view_by_genre(genre):
    """View returns movies filtered by genre"""
    list_films = u.search_by_genre(genre)
    return jsonify(list_films)


@app.errorhandler(404)
def get_404_error(error):
    """404-error handler"""
    return '404 Error'


@app.errorhandler(500)
def get_500_error(error):
    """500-error handler"""
    return '500 Error'


if __name__ == '__main__':
    app.run()
