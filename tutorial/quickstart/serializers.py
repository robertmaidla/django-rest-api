from tutorial.quickstart.models import DataRow, DataSet
from rest_framework import serializers

class DataRowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataRow
        fields = ('id', 'url', 'content')


class DataSetSerializer(serializers.HyperlinkedModelSerializer):
    rows = DataRowSerializer(many=True)
    class Meta:
        model = DataSet
        fields = ('id', 'url', 'name', 'rows')