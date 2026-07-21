from rest_framework import serializers

from materials.models import Course, Lesson, CourseSubscription
from materials.validators import validate_youtube_link
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        max_length=500,
        required=False,
        allow_blank=True,
        validators=[validate_youtube_link],
        help_text="Ссылка на видео. Разрешены только YouTube."
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return CourseSubscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(
        source="lesson_name", many=True
    )  # поскольку related_name=lesson_name, а объектов множество

    def get_lesson_count(self, obj):
        return obj.lesson_name.count()  # поскольку related_name=lesson_name

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
