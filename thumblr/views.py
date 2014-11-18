from thumblr import dto
from thumblr.forms import AddImageForm
from thumblr import usecases
from thumblr.utils.rest import rest_message


def add_image_view(request):
    if request.method == "POST":
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_metadata = dto.ImageMetadata(
                file_name=request.FILES['image'].name,
                site_id=request.POST['site_id'],
                content_type_id=request.POST['content_type'],
                object_id=request.POST['object_id']
            )

            try:
                image_hash = usecases.add_image(
                    request.FILES['image'],
                    image_metadata
                )

                return rest_message(
                    http_status_code=200,
                    status="done",
                    image_hash=image_hash
                )

            except Exception as ex:
                return rest_message(
                    http_status_code=500,
                    status="error",
                    message=str(ex)
                )

        return rest_message(
            http_status_code=500,
            status="error",
            message="invalid form"
        )
    else:
        return rest_message(http_status_code=400,
                            status="Error",
                            message="Only POST accepts")