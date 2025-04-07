from django.shortcuts import render, redirect, get_object_or_404
from WebApp.models import Sign_UpDB,Wishlist
from django.contrib import messages
from AdminApp.models import GenreDB,movieDb
import requests
from django.conf import settings
# Create your views here.


API_KEY = settings.TMDB_API_KEY


def Home_Page(request):
    api=API_KEY
    data=GenreDB.objects.all()[:3]

    return render(request,"Home.html",{'data':data,'api':api})










def Movie(request):
    API_KEY = settings.TMDB_API_KEY
    data1 = GenreDB.objects.all()[:3]
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


    return render(request, "Movies.html", {'movies':data,'category':category,'query':query,'data':data,'data1':data1})




















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
    data= GenreDB.objects.all()[:3]
    genres = GenreDB.objects.all()
    return render(request, "Genre.html", {'Genre': genres,'data':data})



def filtered_genre(request, genre_id):
    data = GenreDB.objects.all()[:3]

    genre_obj = GenreDB.objects.filter(id=genre_id).first()
    if not genre_obj:
        return render(request, "FilteredMovies.html", {
            "genre": "Unknown",
            "movies": [],
            "error": "Genre not found.",
             'data':data

        })

    genre_name = genre_obj.name  # getting the name with the id
    genre_desc = genre_obj.Desc
    API_KEY = settings.TMDB_API_KEY

    # Step 1: Get all genres from TMDB
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}"
    response = requests.get(genre_url)
    tmdb_genres = response.json().get("genres", [])

    # Step 2: Match local genre name with TMDB genre to get its ID
    tmdb_genre_id = None
    for g in tmdb_genres:
        if g["name"].lower() == genre_name.lower():
            tmdb_genre_id = g["id"]
            break

    if not tmdb_genre_id:
        return render(request, "FilteredMovies.html", {
            "genre": genre_name,
            "movies": [],
            "error": "Genre not found in TMDB.",
            'data':data

        })

    # Step 3: Get movies by genre ID
    movie_url = f"https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": tmdb_genre_id
    }
    movie_response = requests.get(movie_url, params=params)
    movies = movie_response.json().get("results", [])

    return render(request, "FilteredMovies.html", {
        "genre": genre_name,
        "genre_desc":genre_desc,
        "movies": movies,
        'data':data
    })




def trending_movies(request):
    data = GenreDB.objects.all()[:3]
    API_KEY = settings.TMDB_API_KEY
    base_URL = "https://api.themoviedb.org/3/movie/"
    url = f"{base_URL}top_rated?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json().get('results', [])  # here is there is no reult we get a empty string
    print(data)

    return render(request,"Trending.html",{'movies':data,'data':data,'data1':data})






def CastList(request):
    data1 = GenreDB.objects.all()[:3]
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

    return render(request, "CastList.html", {"cast": data, "category": category,'data':data,'data1':data1})


def Movie_Details(request, movie_id):
    data = GenreDB.objects.all()[:3]
    API_KEY = settings.TMDB_API_KEY
    base_URL = "https://api.themoviedb.org/3/movie/"

    movie_url = f"{base_URL}{movie_id}?api_key={API_KEY}&append_to_response=credits"
    response = requests.get(movie_url)
    movie_data = response.json()

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

    rating_filter = request.GET.get('rating')
    user_wishlist = Wishlist.objects.filter(user=request.session['Username'])

    # Apply rating filter if selected
    if rating_filter:
        user_wishlist = user_wishlist.filter(my_rating__gte=rating_filter)

    return render(request, "wishlist.html", {"wishlist": user_wishlist, "data": data, "rating_filter": rating_filter})
