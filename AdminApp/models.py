from django.db import models

# Create your models here.
class GenreDB(models.Model):
    name = models.CharField(max_length=60,null=True,blank=True)
    Desc = models.TextField(max_length=250, null=True,blank=True)


class Person(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    role = models.CharField(max_length=50, null=True,blank=True)
    photo = models.ImageField(upload_to='people/', null=True, blank=True)
class movieDb(models.Model):
    name=models.CharField(max_length=40,blank=True,null=True)
    Genre = models.ForeignKey(GenreDB, on_delete=models.CASCADE, related_name="movies")
    Imdb=models.FloatField(blank=True,null=True)
    Image=models.ImageField(upload_to="Movies/",blank=True,null=True)
    Description=models.TextField(max_length=150,blank=True,null=True)
    year=models.IntegerField(null=True,blank=True)
    people = models.ManyToManyField(Person, related_name="movies")


