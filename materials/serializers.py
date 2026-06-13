from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from users.models import Payment


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(
        source="lesson_name", many=True
    )  # поскольку related_name=lesson_name, а объектов множество

    def get_lesson_count(self, obj):
        return obj.lesson_name.count()  # поскольку related_name=lesson_name

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
