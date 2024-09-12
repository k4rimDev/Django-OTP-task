from django.utils.text import slugify


class Uploader:
    
    @staticmethod
    def upload_file(instance, filename):
        return f"order_qr/{slugify(instance.__str__())}/{filename}"
