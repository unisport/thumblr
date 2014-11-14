import json
from django.http import HttpResponse


def rest_message(status=None, http_status_code=200, **kwargs):
    d = {"status": status}
    d.update(kwargs)

    response = HttpResponse(
        json.dumps(d),
        content_type='application/json',
    )
    response.status_code = http_status_code
    return response