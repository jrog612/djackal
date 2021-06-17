from djackal.tests import DjackalAPITestCase
from djackal.views.base import DjackalAPIView
from tests.models import TestModel, TestSerializer


class FilteringTestAPI(DjackalAPIView):
    model = TestModel
    queryset = TestModel.objects.all()
    filter_map = {
        'field_char': 'field_char__contains',
        'field_bool:to_bool': 'field_bool'
    }
    extra_kwargs = {
        'field_int': 1
    }

    def get(self, request):
        kind = request.query_params['kind']
        if kind == 'queryset':
            queryset = self.get_filtered_queryset()
            ser = TestSerializer(queryset, many=True)
        else:
            obj = self.get_object()
            ser = TestSerializer(obj)
        return self.simple_response(ser.data)


class DjackalAPIViewTest(DjackalAPITestCase):
    def test_get_object(self):
        response = self.client.get('/filtering', {'kind': 'object'})
        self.assertStatusCode(404, response)

        obj = TestModel.objects.create(field_int=1)
        TestModel.objects.create(field_int=2)
        TestModel.objects.create(field_int=3)
        TestModel.objects.create(field_int=4)

        response = self.client.get('/filtering', {'kind': 'object'})
        result = response.json()['result']
        self.assertSuccess(response)
        self.assertEqual(result['field_int'], obj.field_int)
        self.assertEqual(result['id'], obj.id)

    def test_get_filtered_queryset(self):
        obj1 = TestModel.objects.create(field_int=1, field_char='char', field_bool=False)
        obj2 = TestModel.objects.create(field_int=1, field_char='chock')
        TestModel.objects.create(field_int=1, field_char='bb')
        TestModel.objects.create(field_int=2, field_char='ch')

        response = self.client.get('/filtering', {'kind': 'queryset', 'field_char': 'ch'})
        result = response.json()['result']

        self.assertSuccess(response)
        self.assertLen(2, result)
        self.assertEqual(obj1.id, result[0]['id'])
        self.assertEqual(obj2.id, result[1]['id'])

        response = self.client.get('/filtering', {'kind': 'queryset', 'field_char': 'char'})
        result = response.json()['result']

        self.assertSuccess(response)
        self.assertLen(1, result)
        self.assertEqual(obj1.id, result[0]['id'])

        response = self.client.get('/filtering', {'kind': 'queryset', 'field_char': 'char', 'field_bool': False})
        result = response.json()['result']

        self.assertSuccess(response)
        self.assertLen(1, result)
        self.assertEqual(obj1.id, result[0]['id'])
