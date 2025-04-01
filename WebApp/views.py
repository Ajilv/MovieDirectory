from django.shortcuts import render, redirect, get_object_or_404
from WebApp.models import Sign_UpDB,Wishlist
from django.contrib import messages
from AdminApp.models import GenreDB,movieDb
import requests
from MovieDirectory import settings
from django.conf import settings
# Create your views here.


API_KEY = settings.TMDB_API_KEY


def Home_Page(request):
    api=API_KEY
    data=GenreDB.objects.all()[:3]

    return render(request,"Home.html",{'data':data,'api':api})


def Blog(request):
    return render(request,"CastList.html")







def Movie(request):
    API_KEY = settings.TMDB_API_KEY
    data = GenreDB.objects.all()[:3]
    category=request.GET.get("category","popular")  # second parameter is the default value
    query = request.GET.get("query")  # Get search Form

    base_URL="https://api.themoviedb.org/3/"

    if query:
        url = f"{base_URL}search/movie?api_key={API_KEY}&query={query}"
    else:
        url = f"{base_URL}movie/{category}?api_key={API_KEY}"

    response = requests.get(url)
    data = response.json().get('results',[])  # here is there is no reult we get a empty string
    print(data)


    return render(request, "Movies.html", {'movies':data,'category':category,'query':query,'data':data})




#
# def Movie(request):
#     genre = request.GET.get('genre', '')
#     year = request.GET.get('year', '')
#
#
#     TMDB_URL = "https://api.themoviedb.org/3/discover/movie"
#     params = {
#         "api_key": settings.TMDB_API_KEY,  # Use API key from settings
#         "language": "en-US",
#         "sort_by": "popularity.desc",
#         "include_adult": "false",
#         "include_video": "false",
#         "page": 1
#     }
#
#     if genre:
#         params["with_genres"] = genre
#     if year:
#         params["primary_release_year"] = year
#
#
#     response = requests.get(TMDB_URL, params=params)
#     movies = response.json().get("results", [])
#
#
#     genre_url = "https://api.themoviedb.org/3/genre/movie/list"
#     genre_response = requests.get(genre_url, params={"api_key": settings.TMDB_API_KEY, "language": "en-US"})
#     genres = genre_response.json().get("genres", [])
#
#     return render(request, "Movies.html", {
#         "data": movies,
#         "genres": genres,
#         "years": range(2024, 2000, -1)
#     })















def User_Sign_Up(request):
    return render(request,"User_Sign_Up.html")

def Save_Sign_Up(request):
    if request.method=="POST":
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        conform_pass = request.POST.get("pass2")
        email = request.POST.get("email")
        obj45=Sign_UpDB(Username=uname,Password=pass1,Conform_Password=conform_pass,Email=email)
        obj45.save()
        messages.success(request,"Register Successfully...!")
        return redirect(User_Sign_In)

def User_Sign_In(request):
    return render(request,"User_Sign_In.html")

def User_Login(request):
    if request.method=="POST":
        un = request.POST.get('username')
        pswd = request.POST.get('pass')
        if Sign_UpDB.objects.filter(Username=un,Password=pswd).exists():
            request.session['Username'] = un
            request.session['Password'] = pswd
            messages.success(request,"Welcome")
            return redirect(Home_Page)
        else:
            messages.warning(request,"User Not Found")
            return redirect(User_Sign_In)
    else:
        messages.warning(request,"Invalid User")
        return redirect(User_Sign_In)

def User_logout(request):
    del request.session['Username']
    del request.session['Password']
    messages.success(request,"Logout Successfully...!")
    return redirect(User_Sign_In)




def Genre(request):
    data= GenreDB.objects.all()

    return render(request,"Genre.html",{'Genre':data})

def filtered_genre(request, genre_id):
    genre = get_object_or_404(GenreDB, id=genre_id)
    movies = movieDb.objects.filter(Genre=genre)
    return render(request, "FilteredGenre.html", {'genre': genre, 'movies': movies,})



def trending_movies(request):
    data = GenreDB.objects.all()[:3]
    API_KEY = settings.TMDB_API_KEY
    base_URL = "https://api.themoviedb.org/3/movie/"
    url = f"{base_URL}top_rated?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json().get('results', [])  # here is there is no reult we get a empty string
    print(data)

    return render(request,"Trending.html",{'movies':data,'data':data})



def Genre(request):
    data = GenreDB.objects.all()[:3]
    API_KEY = settings.TMDB_API_KEY
    category=request.GET.get("genre","popular")  # second parameter is the default value
    base_URL="https://api.themoviedb.org/3/movie/"
    url = f"{base_URL}{category}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json().get('results',[])  # here is there is no reult we get a empty string
    print(data)
    return render(request, "Movies.html", {'movies':data,'category':category,'data':data})





def CastList(request):
    data = GenreDB.objects.all()[:3]
    API_KEY = settings.TMDB_API_KEY  # Your TMDb API key
    category = request.GET.get("category", "popular")  # Default category is 'popular'
    base_url = "https://api.themoviedb.org/3/person/"
    # Define the API endpoint based on category
    if category == "popular":
        url = f"{base_url}popular?api_key={API_KEY}"
    elif category == "trending":
        url = f"https://api.themoviedb.org/3/trending/person/week?api_key={API_KEY}"
    else:
        url = f"{base_url}popular?api_key={API_KEY}"  # Default to popular cast if category is unknow
    # Fetch data from TMDb API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('results', [])
    else:
        data = []  # If API fails, return an empty list

    return render(request, "CastList.html", {"cast": data, "category": category,'data':data})


def Movie_Details(request, movie_id):
    data = GenreDB.objects.all()[:3]
    API_KEY = settings.TMDB_API_KEY
    base_URL = "https://api.themoviedb.org/3/movie/"

    # Fetch movie details with cast information
    movie_url = f"{base_URL}{movie_id}?api_key={API_KEY}&append_to_response=credits"
    response = requests.get(movie_url)
    movie_data = response.json()

    # Extract main cast (limit to 5 actors)
    cast_list = [cast["name"] for cast in movie_data.get("credits", {}).get("cast", [])[:5]]

    context = {
        'movie': movie_data,
        'cast': cast_list,
        'data': data
    }

    return render(request, "movie_details.html", context)



def add_to_wishlist(request, movie_id):

    if 'Username' not in request.session:
        messages.warning(request, "You need to log in first.")
        return redirect('User_Sign_In')

    if request.method == "POST":
        my_rating = request.POST.get('my_rating')
        my_review = request.POST.get('my_review')
        movie_image = request.POST.get('movie_image')
        movie_people = request.POST.get('movie_people')


        # Fetch movie details
        API_KEY = settings.TMDB_API_KEY
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(movie_url)
        movie_data = response.json()

        Wishlist.objects.create(
            user=request.session['Username'],
            movie_id=movie_data['id'],
            movie_name=movie_data['title'],
            movie_genre=", ".join([genre['name'] for genre in movie_data.get('genres', [])]),
            movie_rating=movie_data.get('vote_average'),
            description=movie_data.get('overview'),
            my_rating=my_rating,
            my_review=my_review,
            M_image = movie_image,
            cast=movie_people
        )

        messages.success(request, "Movie added to wishlist!")
        return redirect('Movie_Details', movie_id=movie_id)


def view_wishlist(request):
    data = GenreDB.objects.all()[:3]
    if 'Username' not in request.session:
        messages.warning(request, "You need to log in first.")
        return redirect('User_Sign_In')

    user_wishlist = Wishlist.objects.filter(user=request.session['Username'])
    return render(request, "wishlist.html", {"wishlist": user_wishlist,'data':data})
