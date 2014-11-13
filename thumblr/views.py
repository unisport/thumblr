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
                file_type=request.POST['image_type'],
            )

            try:
                image_hash = usecases.add_image(
                    request.FILES['image'],
                    image_metadata
                )

                return rest_message(
                    status="done",
                    image_hash=image_hash
                )

            except Exception as ex:
                return rest_message(
                    status="error",
                    message=str(ex)
                )

        return rest_message(
            status="error",
            message="invalid form"
        )