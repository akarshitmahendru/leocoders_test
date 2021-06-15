import io
import csv

from django.db import transaction
from django.http import Http404
from rest_framework import generics, response, status, permissions
from .models import CSVModel
from .serializers import UploadSerializer, CSVImportSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class UploadAPIView(generics.CreateAPIView):
    """
        API to upload data in csv format
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UploadSerializer
    model = CSVModel

    def get_csv_data_validated(self, csv_data):
        serializer = CSVImportSerializer(data=csv_data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data, True
        else:
            return serializer.errors, False

    def post(self, request, *args, **kwargs):
        if request.FILES:
            csvfile = request.FILES['csv_file']
            if not csvfile.name.endswith('.csv'):
                raise Http404
        else:
            return response.Response("{'msg':'no file detected'}")
        csvfile = csvfile.read().decode('utf-8')
        io_string = io.StringIO(csvfile)
        reader = csv.reader(io_string, delimiter=',')
        header_cols = next(reader)
        total_row_count = 0

        for line in reader:
            with transaction.atomic():
                obj = {
                    "symbol": line[1],
                    "date": line[2],
                    "open": float(line[3]),
                    "high": float(line[4]),
                    "low": float(line[5]),
                    "close": float(line[6]),
                    "volume": int(line[7]),
                    "adj_close": float(line[8]),
                }
                total_row_count += 1
            try:
                validated_data, success = self.get_csv_data_validated(obj)
                print(validated_data, success)
                if success:
                    validated_data.update({"created_by": self.request.user.id})
                    self.model.objects.create(**validated_data)
                else:
                    print(validated_data)
                    continue
            except Exception as e:
                line.append(e.args[0].__str__())
                print("error: %s" % str(e.args[0]))
                print(line)
                continue
        return response.Response(
            {'msg': 'File successfully uploaded'},
            status=status.HTTP_201_CREATED
        )
