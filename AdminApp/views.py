from django.shortcuts import render,redirect
from AdminApp.models import movieDb,Person,GenreDB
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
# Create your views here.
def index(request):
    return render(request,"index.html")


def add_movies(request):
    gdata=GenreDB.objects.all()
    people = Person.objects.all()
    return render(request,"Add_movies.html",{"gdata":gdata,"people":people})


def save_movies(request):
    if request.method=="POST":
        name=request.POST.get('mname')
        genre=request.POST.get('genre')
        rate=request.POST.get('rate')
        mdescr=request.POST.get('mdescr')
        mpic=request.FILES['mpic']

        year=request.POST.get('year')
        people_ids = request.POST.getlist("people")


        obj1=movieDb(name=name,Genre=genre,Imdb=rate,Description=mdescr,Image=mpic,year=year)
        obj1.save()
        obj1.people.set(people_ids)
        return redirect(index)


def view_moviews(request):
    data=movieDb.objects.all()
    return render(request,"View_movies.html",{'data':data})
def del_movies(request,mid):
    obj1=movieDb.objects.all()
    obj1.delete()
    return redirect(view_moviews)

def Edit_movies(request,mid):
    data=movieDb.objects.get(id=mid)
    return render(request,"Edit_Movie.html",{'data':data})








def add_genre(request):
    return render(request,"Add_genre.html")


def save_genre(request):
    if request.method=="POST":
        name=request.POST.get('gname')
        desc=request.POST.get('gdescr')
        obj=GenreDB(name=name,Desc=desc)
        obj.save()
        return redirect(index)

def view_genre(request):
    data=GenreDB.objects.all()
    return render(request,"View_genre.html",{'data':data})

def loginpage(request):
    return render(request,"login_page.html")


def Admin_login(request):
    if request.method=="POST":
        un = request.POST.get('username')
        pswd = request.POST.get('pass')
        if User.objects.filter(username__contains=un).exists():
            x= authenticate(username=un,password = pswd)
            if  x is not None:
                request.session['username']=un
                request.session['password']=pswd
                login(request, x)
                return redirect(index)
            else:

                return redirect(loginpage)
        else:
            return redirect(loginpage)



def Admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(loginpage)






#---------------------------------------------------------------------------------

def add_person(request):
    return render(request, 'add_person.html')

def save_person(request):
    if request.method == "POST":
        name = request.POST.get('name')
        role = request.POST.get('role')
        photo = request.FILES.get('photo')  # Getting uploaded image


        person = Person(name=name, role=role, photo=photo)
        person.save()

        return redirect('list_persons')

    return redirect('add_person')

def list_persons(request):
    persons = Person.objects.all()
    return render(request, 'list_person.html', {'persons': persons})

def delete_person(request, person_id):
    person = Person.objects.get(id=person_id)
    person.delete()
    return redirect('list_persons')