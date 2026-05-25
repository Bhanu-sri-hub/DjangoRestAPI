from rest_framework import serializers

from watchlist_app.models import WatchList, StreamPlatform, Review
class ReviewSerializer(serializers.ModelSerializer):
    review_user= serializers.StringRelatedField(read_only=True)
    #watchlist = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        #fields="__all__"
        exclude = ('watchlist',)
       # read_only_fields = ['watchlist']
class WatchListSerializer(serializers.ModelSerializer):
    #reviews = serializers.StringRelatedField(read_only= True, many= True)
    reviews = ReviewSerializer(read_only = True, many = True)
    class Meta:
        model = WatchList
        #fields = ['id','monthname','challenge']
        fields = "__all__"
        #read_only_fields = ['avg_rating', 'numb_of_ratings']
        #exclude = ['active']

#class StreamPlatformSerializer(serializers.ModelSerializer):
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    #watchlist = WatchListSerializer(many=True, read_only=True) used to get all info
    #watchlist = serializers.StringRelatedField(many=True, read_only = True)
    #watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #watchlist = serializers.HyperlinkedRelatedField(many=True, read_only= True, view_name = "watch-detail") --> line used in ModelSerializers
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        #fields = ['id','monthname','challenge']
        fields = "__all__"
        depth = 1





'''

Creating Serializers with only serializers 


class MonthlySerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only= True)
    monthname = serializers.CharField(max_length = 50)
    challenge=serializers.CharField()
    active = serializers.BooleanField(default = True)

    def create(self, validated_data):
        return MonthlyChallenge.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.monthname = validated_data.get('monthname', instance.monthname)
        instance.challenge = validated_data.get('challenge', instance.challenge)
        instance.save()
        return instance
'''