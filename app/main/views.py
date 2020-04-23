from flask import render_template,request,redirect,url_for
from . import main
from ..requests import get_movies,get_movie,search_movie
from ..models import Review
from .forms import ReviewForm

# Review=reviews.Review
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    upcoming_movies=get_movies('upcoming')
    now_playing_movies=get_movies('now_playing')
    popular_movies=get_movies('popular')
    print(popular_movies)
    title="Watchlist."
    search_movie=request.args.get('movie_query')
    if search_movie:
        return redirect(url_for('main.search',movie_name=search_movie))

    else:

        return render_template('index.html',message=title,popular=popular_movies,upcoming=upcoming_movies,now_playing=now_playing_movies)

@main.route('/movies/<int:id>')
def movies(id):

    movie=get_movie(id)
    reviews=Review.get_reviews(movie.id)
    title=f'{movie.title}'
    return render_template('movies.html',title=title, movie=movie,reviews=reviews)

@main.route('/search/<movie_name>')
def search(movie_name):
    movie_name_list=movie_name.split(' ')
    movie_name_format='+'.join(movie_name_list)
    searched_movies=search_movie(movie_name_format)
    title=f'search results for {movie_name}'

    return render_template('search.html',movies=searched_movies)


@main.route('/movies/review/new/<int:id>', methods=['GET','POST'])
def new_review(id):
    form =ReviewForm()
    movie=get_movie(id)

    if form.validate_on_submit():
        title=form.title.data
        review=form.review.data
        new_review=Review(movie.id,title,movie.poster,review)
        new_review.save_review()
        return redirect(url_for('main.movies',id=movie.id))

    title=f'{movie.title} review'
    return render_template('new_review.html',title=title,review_form=form,movie=movie)