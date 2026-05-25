from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.views import APIView
from watchlist_app.api.permissions import AdminorReadOnly, ReviewUserOrReadOnly
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchlistobj = WatchList.objects.get(pk=pk)
        cur_review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist = watchlistobj, review_user = cur_review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed the movie..!")
        if watchlistobj.numb_of_ratings == 0:
            watchlistobj.avg_rating = serializer.validated_data['rating']

        else:
            watchlistobj.numb_of_ratings+=1
            watchlistobj.avg_rating = (watchlistobj.avg_rating+ serializer.validated_data['rating'])/watchlistobj.numb_of_ratings
        watchlistobj.save()
        
        return serializer.save(watchlist = watchlistobj, review_user= cur_review_user)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    def get_queryset(self):
        pk = self.kwargs['pk']
        index = self.kwargs['index'] # Overwriting query set
        return Review.objects.filter(watchlist=index,pk=pk)
    

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated] --> inbuilt method
    
    def get_queryset(self):
        pk = self.kwargs['pk'] # Overwriting query set
        return Review.objects.filter(watchlist=pk)
    

'''
class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

'''  
    

class WatchListAV(APIView):
    def get(self, request):
        try:
            watchlist = WatchList.objects.all()
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
   def get(self, request,pk):
        try:
            watchdetail = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = WatchListSerializer(watchdetail)
        return Response(serializer.data)
   
   def put(self, request,pk):
       watchdetail = WatchList.objects.get(pk=pk)
       serializer = WatchListSerializer(watchdetail, data=request.data)
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
       else:
            return Response(serializer.errors)    
   def delete(self, request,index):
        watchdetail = WatchList.objects.get(pk=index)
        watchdetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#streamPlatform with viewset 
class StreamPlatformVS(viewsets.ViewSet):
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True,  context ={"request": request} )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(user ,  context ={"request": request} )
        return Response(serializer.data)

class StreamPlatformAV(APIView):
    def get(self, request):
        try: 
            platform = StreamPlatform.objects.all()
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, many=True, context ={"request": request} )
        return Response(serializer.data)
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatformDetailAV(APIView):
   def get(self, request,pk):
       try: 
            streamplatform = StreamPlatform.objects.get(pk=pk)
       except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
       serializer = StreamPlatformSerializer(streamplatform, context ={"request": request})
       return Response(serializer.data)
   
   def put(self, request,pk):
       streamplatform = StreamPlatform.objects.get(pk=pk)
       serializer =StreamPlatformSerializer(streamplatform, data=request.data, context ={"request": request})
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
       else:
            return Response(serializer.errors)    
   def delete(self, request,pk):
        streamplatform = StreamPlatform.objects.get(pk=pk)
        streamplatform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


           
'''
class MonthList(APIView):


    def get(self, request):
        monthlist = MonthlyChallenge.objects.all()
        mserializer = MonthlySerializers(monthlist, many=True)
        return Response(mserializer.data)


    def post(self, request):
        serializer = MonthlySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class MonthlyDetailChallenge(APIView):
    def get(self, request, index):
        monthlydescription = MonthlyChallenge.objects.get(pk=index)
        serializer = MonthlySerializers(monthlydescription)
        return Response(serializer.data)
    def put(self, request, index):
        monthdata = MonthlyChallenge.objects.get(pk=index)
        serializer = MonthlySerializers(monthdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self, request,index):
        monthdata = MonthlyChallenge.objects.get(pk=index)
        monthdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




This implementation is with HTTP without REST API serializers
def monthlist(request):
    months = MonthlyChallenge.objects.all()
    data = {
        'monthslist' : list(months.values())
    }
    return JsonResponse(data)





This is Function based views
@api_view(['GET','POST'])
def monthnameslist(request):
    if request.method == "GET":
        monthlist = MonthlyChallenge.objects.all()
        mserializer = MonthlySerializers(monthlist, many=True)
        return Response(mserializer.data)
    if request.method == "POST":
        serializer = MonthlySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            



@api_view(['GET','PUT','DELETE'])
def month(request,index):
    if request.method == "GET":
        monthlydescription = MonthlyChallenge.objects.get(pk=index)
        serializer = MonthlySerializers(monthlydescription)
        return Response(serializer.data)
    elif request.method == 'PUT':
        monthdata = MonthlyChallenge.objects.get(pk=index)
        serializer = MonthlySerializers(monthdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == "DELETE":
        monthdata = MonthlyChallenge.objects.get(pk=index)
        monthdata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        


# def index(request):
#     return render(request,"blog/index.html",{"months":months})


'''




