from flask import Flask, render_template, request, redirect, make_response
from googlemovieshowtimes import GoogleMovieShowtimes

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        postal_code = request.cookies.get('postal_code')
        return render_template('first_page.html', postal_code=postal_code)
    elif request.method == 'POST':
        postal_code = request.form.get('postal_code')
        theater = request.form.get('Theater')
        if postal_code and theater:
            movie = GoogleMovieShowtimes(postal_code, '', theater)
            theaters = movie.parse()
            cinemas = theaters.get('theater')
            cinema = cinemas[0]
            movies = cinema.get('movies')
            ret = make_response(render_template('movie_list.html', movies=movies))
            ret.set_cookie('postal_code', postal_code)
            return ret
        else:
            return redirect('/')

if __name__ == '__main__':
    app.run()
