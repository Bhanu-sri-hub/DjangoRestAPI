from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV, StreamPlatformVS,  ReviewList, ReviewDetail, ReviewCreate)
router = DefaultRouter()
router.register('stream',StreamPlatformVS, basename="streamplatform")
urlpatterns = [
    path("list/",WatchListAV.as_view(),name="watchlist"),
    path("<int:pk>/",WatchDetailAV.as_view(), name="watch-detail"),
    path('',include(router.urls)),
    #path("stream/",StreamPlatformAV.as_view(), name="streamplatform"),
    #path("stream/<int:pk>",StreamPlatformDetailAV.as_view(), name="streamplatform-detail"),
    path("<int:pk>/review/", ReviewList.as_view(), name="review"),
    
    path("<int:index>/review/<int:pk>", ReviewDetail.as_view(), name="review-detail"),
    path("<int:pk>/review-create", ReviewCreate.as_view(), name='review-create')
    #path("review/", ReviewList.as_view(), name = "reviewlist"),
    #path("review/<int:pk>", ReviewDetail.as_view(), name= "review-detail")


]
