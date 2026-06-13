from rest_framework import serializers
from urllib.parse import urlparse


def validate_youtube_link(value):

    parsed_url = urlparse(value.strip())

    domain = parsed_url.netloc

    if 'youtube.com' not in domain:
        raise serializers.ValidationError(
            "Ссылка недопустима. Разрешены только видео с YouTube (домен youtube.com)."
        )

    return value