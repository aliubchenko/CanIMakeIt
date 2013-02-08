from flask import Flask, render_template, request, redirect, url_for
from googlemovieshowtimes import GoogleMovieShowtimes

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('first_page.html')
    elif request.method == 'POST':
        postal_code = request.form.get('postal_code')
        theater = request.form.get('Theater')
        if postal_code and theater:
            movie = GoogleMovieShowtimes(postal_code, '', theater)
            theaters = movie.parse()
            cinemas = theaters.get('theater')
            cinema = cinemas[0]
            movies = cinema.get('movies')
            return render_template('movie_list.html', movies=movies)
        else:
            return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
