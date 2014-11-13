import json
from django.http import HttpResponse


def rest_message(status=None, **kwargs):
    d = {"status": status}
    d.update(kwargs)

    return HttpResponse(
        json.dumps(d),
        content_type='application/json'
    )