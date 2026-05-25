from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class StreamPlatform(models.Model):

    

    class Meta:
        verbose_name = "StreamPlatform"
        verbose_name_plural = "StreamPlatforms"

    name = models.CharField(max_length=50)
    about = models.CharField(max_length=100)
    website = models.URLField(max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("StreamPlatform_detail", kwargs={"pk": self.pk})


class WatchList(models.Model):
    
    class Meta:
        verbose_name = "WatchList"
        verbose_name_plural = "WatchLists"
    title = models.CharField(max_length= 50)
    description = models.CharField(max_length=200)
    platformtostream = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name= 'watchlist')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)
    numb_of_ratings= models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("WatchList_detail", kwargs={"pk": self.pk})
class Review(models.Model):

    

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=150, null=True)
    watchlist = models.ForeignKey(WatchList, related_name='reviews', on_delete=models.CASCADE)
    active = models.BooleanField(default= True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.rating)+ " | "+ self.watchlist.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


'''
class MonthlyChallenge(models.Model):

    

    class Meta:
        verbose_name = "MonthlyChallenge"
        verbose_name_plural = "MonthlyChallenges"
    monthname = models.CharField()
    challenge = models.CharField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.monthname

    # def get_absolute_url(self):
    #     return reverse("MonthlyChallenge_detail", kwargs={"pk": self.pk})

    
    '''