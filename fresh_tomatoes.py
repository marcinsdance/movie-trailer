#!/usr/bin/env python
import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  {head}
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies), head=main_page_head)

  # Output the file
  output_file.write(rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

# New 'Movie' class created to provide a thumbnail for the movie instances
class Movie:
	trailer_youtube_url = ""
	title = ""
	poster_image_url = ""

# "Limitless" - new moview
movie1 = Movie()
movie1.title = "Limitless"
movie1.poster_image_url = "http://cdn.movieweb.com/img.backdrops/FRb4u7HS71YJeg_1_a.jpg"
movie1.trailer_youtube_url = "https://www.youtube.com/watch?v=QqMe6pwSfIE"

# "Burnt" - new moview
movie2 = Movie()
movie2.title = "Burnt"
movie2.poster_image_url = "http://e.movie.as/p/246390.jpg"
movie2.trailer_youtube_url = "https://www.youtube.com/watch?v=QsyzkkI_g14"

# "Only Lovers Left Alive" - new moview
movie3 = Movie()
movie3.title = "Only Lovers Left Alive"
movie3.poster_image_url = "http://ia.media-imdb.com/images/M/MV5BMTY0NTQ1NjA0OV5BMl5BanBnXkFtZTgwMDg5NjkzMTE@._V1__SX1859_SY916_.jpg"
movie3.trailer_youtube_url = "https://www.youtube.com/watch?v=ycOKvWrwYFo"

# "Himalaya" - new moview
movie4 = Movie()
movie4.title = "Himalaya"
movie4.poster_image_url = "http://1.fwcdn.pl/po/13/71/1371/6928413.3.jpg"
movie4.trailer_youtube_url = "https://www.youtube.com/watch?v=vN--9D7rmlQ"

# "Robin Hood: Men in Tights" - new moview
movie5 = Movie()
movie5.title = "Robin Hood: Men in Tights"
movie5.poster_image_url = "https://www.movieposter.com/posters/archive/main/99/MPW-49670"
movie5.trailer_youtube_url = "https://www.youtube.com/watch?v=dX4Ik-cyp-I"

# "Robin Hood" - new moview
movie6 = Movie()
movie6.title = "Robin Hood"
movie6.poster_image_url = "http://1.fwcdn.pl/po/06/61/430661/7326376.3.jpg"
movie6.trailer_youtube_url = "https://www.youtube.com/watch?v=fQ6zXDSgwIY"

# 'movies' list stores all movie objects
movies = [movie1, movie2, movie3, movie4, movie5, movie6]

# Finally execute the script and launch the page
open_movies_page(movies);