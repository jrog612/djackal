from djackal.shortcuts import model_update

__all__ = [
    'ListViewMixin',
    'CreateViewMixin',
    'DetailViewMixin',
    'UpdateViewMixin',
    'DestroyViewMixin',
]


class ListViewMixin:
    def list(self, request, **kwargs):
        filtered_queryset = self.get_filtered_queryset()

        if self.paging:
            paginate_queryset = self.get_paginate_queryset(filtered_queryset)
            ser = self.get_serializer(paginate_queryset, many=True)
            meta = self.get_paginated_meta()
            return self.simple_response(ser.data, meta=meta)

        ser = self.get_serializer(filtered_queryset, many=True)
        return self.simple_response(ser.data)


class CreateViewMixin:
    def create(self, request, **kwargs):
        model = self.get_model()
        obj = model(**self.get_inspected_data())
        if self.bind_user_field:
            setattr(obj, self.bind_user_field, self.binding_user())
        obj.save()
        return self.simple_response({'id': obj.id})


class DetailViewMixin:
    def detail(self, request, **kwargs):
        obj = self.get_object()
        ser = self.get_serializer(obj)
        return self.simple_response(ser.data)


class UpdateViewMixin:
    def update(self, request, **kwargs):
        obj = self.get_object()
        model_update(obj, **self.get_inspected_data())
        return self.simple_response({'id': obj.id})


class DestroyViewMixin:
    def destroy(self, request, **kwargs):
        obj = self.get_object()
        obj.delete()
        return self.simple_response()
