from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from users.models import Payment


class LessonSerializer(ModelSerializer):
    courses = SerializerMethodField()

    def get_courses(self, lesson):
        return [course.course_name for course in Course.objects.filter(lesson=lesson)]

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    lesson = LessonSerializer()
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    quantity_lessons_in_course = SerializerMethodField()
    lesson = LessonSerializer()

    def get_quantity_lessons_in_course(self, course):
        return Course.objects.filter(lesson=course.lesson).count()

    class Meta:
        model = Course
        fields = ("course_name", "quantity_lessons_in_course")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
