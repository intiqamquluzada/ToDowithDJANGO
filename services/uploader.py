class Uploader:

    @staticmethod
    def upload_images_to_profile(instance, filename):
        return f"profile/{instance.slug}/{filename}"
