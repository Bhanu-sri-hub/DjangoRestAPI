from django.urls import path
from watchlist_app import views

urlpatterns = [
    path("list",views.monthlist,name="monthnamelist")
]
