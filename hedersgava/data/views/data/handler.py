"""The data handler"""
import datetime
import dateutil.parser
from django.views.defaults import bad_request
from django import http
from rest_framework.response import Response
from rest_framework.views import APIView
from . import xml_parser
from ...models import data_record, data_set, device


class DataView(APIView):
    """A view for data"""
    parser_classes = (xml_parser.XMLParser,)

    def post(self, request, format=None):
        """Handle POST"""
        data = request.data

        data_set_id = data['id']
        datetime_obj = datetime.datetime.fromtimestamp(data['record_time'])

        # Query the device model. And create the mapping for device_id -> device model object.
        dev_map = {}
        for dev_id, dev_type in data['devices'].items():
            dev_obj, created = device.Device.objects.get_or_create(
                type=dev_type,
                device_id=dev_id,
            )
            dev_obj.save()
            dev_map[dev_obj.device_id] = dev_obj

        # Create the data set.
        data_set_obj = data_set.DataSet(id=data_set_id)
        data_set_obj.save()

        # Create the data record.
        for data_item in data['data']:
            dev_obj = dev_map.get(data_item['device'], None)
            if dev_obj is None:
                return http.HttpResponseBadRequest()
            data_record_obj = data_record.DataRecord(
                datetime=datetime_obj,
                data_set=data_set_obj,
                device=dev_obj,
                value=data_item['value']
            )
            data_record_obj.save()

        return Response()

    def get(self, request, format=None):
        """Handle GET"""
        result = []
        query_set = data_record. DataRecord.objects.all()

        # When the <id> provided, the <id> will be considered as the datetime or timestamp.
        # And will filter the data by this parameter.
        if format is not None and format != '':
            if format.isdigit():  # If the parameter is a digit, it will be considered as timestamp.
                target_datetime = datetime.datetime.fromtimestamp(int(format))
            else:
                try:
                    target_datetime = dateutil.parser.parse(format)
                except ValueError as exc:
                    return http.HttpResponseBadRequest()
            query_set = query_set.filter(datetime=target_datetime)

        for record in query_set:
            result.append(
                {
                    'datetime': record.datetime.isoformat(),
                    'value': record.value,
                    'unit': record.device.unit
                }
            )
        return http.JsonResponse(result, safe=False)
