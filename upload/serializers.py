from rest_framework import serializers

from upload.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
