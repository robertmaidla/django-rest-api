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
        try:
            uploaded_file = request.FILES['file']
            autoMod = DataSet(name = uploaded_file.name)
            autoMod.save()
            while True:
                line = uploaded_file.readline()
                if not line: break
                newRow = DataRow(content= str(line))
                newRow.save()
                autoMod.rows.add(newRow)
            return Response(autoMod.pk, status=status.HTTP_201_CREATED)
        except:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    # Get the rows of a specific DataSet
    @action(detail=True, methods=['get'])
    def rows(self, request, pk=None):
        dataSet = self.get_object()
        rows = DataRow.objects.filter(dataset=dataSet)
        serializer = DataRowSerializer(rows, many=True, context={'request': request})
        return Response(serializer.data,status=200)

# Remove the connection to selected DataRow in DataSet
# NB! NO VALIDATION HERE (GET REQUESTS CAN MODIFY DATA)
def remove_row(request, set_key, row_key):
    dataSet = DataSet.objects.filter(id=set_key).get()
    rowToRemove = DataRow.objects.filter(id=row_key).get()
    dataSet.rows.remove(rowToRemove)
    return JsonResponse({})