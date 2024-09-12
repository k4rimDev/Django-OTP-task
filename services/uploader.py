from django.utils.text import slugify


class Uploader:
    
    @staticmethod
    def upload_file(instance, filename):
        return f"files/{slugify(instance.__str__())}/{filename}"
