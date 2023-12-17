from rest_framework import serializers

from .models import *


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = "__all__"


class BoxCustomSerializer(serializers.ModelSerializer):
    regionfrom__name = serializers.CharField(source='regionfrom.name', read_only=True)
    regionto__name = serializers.CharField(source='regionto.name', read_only=True)
    class Meta:
        model = Boxes
        fields = (
            'id','clientfrom', 'clientto','phonefrom','phoneto', 'addressfrom','addressto',
            'tarif','amount','weight','volumesm','delivery','minsm','maxsm','placecount','discount',
            'valuta','status','comment','select','payment','boximg','regionfrom__name', 'regionto__name',
            'regionfrom', 'regionto','inputdate', 'updatedate', 'user'
        )
        # depth = 1


class BoxesSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # region_name = serializers.ManyRelatedField(source='region.name', child_relation='region')
    
    class Meta:
        model = Boxes
        fields = '__all__'


class BoxHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxHistory
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__" 


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"