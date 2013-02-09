"""
Google Movie Showtimes parser class for Python.

This script provides a Python class that can be used to parse Google Movie
Showtimes (www.google.com/movies) pages into dictionary objects.

@author Vaidik Kapoor
@version 0.1
"""

import urllib
import re
from copy import deepcopy
from urllib2 import Request, urlopen, URLError

from BeautifulSoup import BeautifulSoup


class GoogleMovieShowtimes:
    """
    Constructor for GoogleMovieShowtimes class.

    Parameters:
        near (optional)     - (string) valid name of the location (city)
        mid	(optional)      - (string) valid movie ID. Can be taken from
                              www.google.com/movies
        tid	(optional)      -	(string) valid theater ID. Can be taken from
                              www.google.com/movies

    GoogleMovieShowtimes class
	This class is used for getting response from www.google.com/movies
    """

    def __init__(self, near, mid, tid):
        """

        :param near:
        :param mid:
        :param tid:
        """
        self.params = {'near': near, 'mid': mid, 'tid': tid}

        params = deepcopy(self.params)
        for key, val in params.iteritems():
            if val == '':
                self.params.pop(key)
        params = urllib.urlencode(self.params)

        url = 'http://www.google.com/movies?'
        req = Request(url, params)
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            # everything is fine
            self.response_body = response.read()
            self.html = BeautifulSoup(self.response_body)


    def parse(self):
        """
        Function for parsing the response and getting all the important data
        as a huge dictionary object.

        No parameters are required.
        """
        if 'mid' in self.params:
            resp = {'movie': []}
            movies = self.html.findAll('div', attrs={'class': 'movie'})
            for div in movies:
                resp['movie'].append({})

                index = resp['movie'].index({})

                movie = []

                movie.append(('name', div.div.h2.contents[0]))
                movie.append(('info', div.div.find('div', attrs={'class': 'info'})))
                movie.append(('info_links', div.div.find('div', attrs={'class': 'links'})))
                movie.append(('theater', []))

                resp['movie'][index] = dict(movie)

                theaters = div.findAll('div', {'class': 'theater'})
                for div_theater in theaters:
                    resp['movie'][index]['theater'].append({})

                    index_th = resp['movie'][index]['theater'].index({})

                    theater = []

                    name = div_theater.div.find(attrs={'class': 'name'}).a.contents[0]
                    theater.append(('name', name))

                    theater.append(('address', div_theater.div.find(attrs={'class': 'address'}).contents[0]))
                    theater.append(('times', []))

                    resp['movie'][index]['theater'][index_th] = dict(theater)

                    times = div_theater.find('div', {'class': 'times'})
                    times = times.findAll('span')
                    for div_time in times:
                        if len(div_time.contents) == 3:
                            time_val = div_time.contents[2]
                            time_val = re.search('(.*)&#', time_val)

                            resp['movie'][index]['theater'][index_th]['times'].append(time_val.group(1))

            return resp

        resp = {'theater': []}
        theaters = self.html.findAll('div', attrs={'class': 'theater'})
        for entry in theaters:
            if 'closure' in entry.span.attrs[0]:
                continue

            resp['theater'].append({})

            index = resp['theater'].index({})

            theater = []
            theater.append(('name', entry.div.h2.contents[0]))
            theater.append(('info', entry.div.div.contents[0]))
            theater.append(('movies', []))

            resp['theater'][index] = dict(theater)

            movies = entry.findAll('div', {'class': 'movie'})
            for div_movie in movies:
                resp['theater'][index]['movies'].append({})

                index_m = resp['theater'][index]['movies'].index({})

                movie = [('name', div_movie.div.a.contents[0]), ('info', div_movie.span.contents[0]), ('times', [])]

                resp['theater'][index]['movies'][index_m] = dict(movie)

                times = div_movie.find('div', {'class': 'times'})
                times = times.findAll('span')
                for div_time in times:
                    if len(div_time.contents) == 3:
                        time_val = div_time.contents[2]
                        # time_val = re.search('(.*)&#', time_val)
                        if time_val:
                            time_val = re.search(r'(\d+:\d+)', time_val).group(1)

                        resp['theater'][index]['movies'][index_m]['times'].append(time_val)

        return resp