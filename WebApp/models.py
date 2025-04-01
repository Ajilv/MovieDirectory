from django.db import models

# Create your models here.


class Sign_UpDB(models.Model):
    Username=models.CharField(max_length=150,null=True,blank=True)
    Password=models.CharField(max_length=150,null=True,blank=True)
    Conform_Password=models.CharField(max_length=150,null=True,blank=True)
    Email=models.EmailField(max_length=150,null=True,blank=True)


class Wishlist(models.Model):
    user = models.CharField(max_length=70, null=True, blank=True)
    movie_id = models.IntegerField(null=True, blank=True)
    movie_name = models.CharField(max_length=100, null=True, blank=True)
    movie_genre = models.CharField(max_length=100, null=True, blank=True)
    movie_rating = models.FloatField(null=True, blank=True)
    cast = models.TextField(max_length=200,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    my_rating = models.IntegerField(null=True, blank=True)
    my_review = models.TextField(null=True, blank=True)
    M_image = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.movie_name}"

