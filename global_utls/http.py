from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder


class JsonResponse(HttpResponse):
    def __init__(self, data, request=None):
        _content = json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder)
        if request is not None and request.GET.get('callback') is not None:
            callback = request.GET.get('callback')
            _content = '%s(%s);'% (callback,_content)
            super(JsonResponse, self).__init__(content=_content,
                                               mimetype="application/javascript; charset=utf-8")
        else:
            super(JsonResponse, self).__init__(content=_content,
                                               mimetype="application/json; charset=utf-8")


class JSResponse(HttpResponse):
    def __init__(self, data):
        super(JSResponse, self).__init__(content=data,
                                         mimetype="application/x-javascript; charset=utf-8")


class CssResponse(HttpResponse):
    def __init__(self, data):
        super(CssResponse, self).__init__(content=data,
                                         mimetype="text/css")

