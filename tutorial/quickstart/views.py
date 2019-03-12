from tutorial.quickstart.models import DataRow, DataSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from tutorial.quickstart.serializers import DataRowSerializer, DataSetSerializer
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers


class DataRowViewSet(viewsets.ModelViewSet):
    queryset = DataRow.objects.all()
    serializer_class = DataRowSerializer


class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

    # Generate and link new DataSet and DataRow objects
    @action(detail=False, methods=['post'])
    def generate(self, request, pk=None):
        print("############ PRINT ###########")
        # print(request)
        # print(request.data)
        uploaded_file = request.FILES['file']
        while True:
            line = uploaded_file.readline()
            if not line:
                break
            print(line)
            # Get the 3 line values from here
        print("############ PRINT ###########")
        requestName = request.data.get('name')
        requestRows = request.data.get('rows')
        autoMod = DataSet(name = requestName)
        autoMod.save()
        serializer = DataRowSerializer(data=requestRows, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            for newRow in serializer.data:
                autoMod.rows.add(list(newRow.values())[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get the rows of a specific DataSet
    @action(detail=True, methods=['get'])
    def rows(self, request, pk=None):
        dataSet = self.get_object()
        rows = DataRow.objects.filter(dataset=dataSet)
        serializer = DataRowSerializer(rows, many=True, context={'request': request})
        return Response(serializer.data,status=200)

# Remove the connection to selected DataRow in DataSet
def remove_row(request, set_key, row_key):
    dataSet = DataSet.objects.filter(id=set_key).get()
    rowToRemove = DataRow.objects.filter(id=row_key).get()
    dataSet.rows.remove(rowToRemove)
    return JsonResponse({})