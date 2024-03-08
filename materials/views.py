from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.permissions import IsModerator, IsOwner
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.utils import timezone

from .services import course
from .tasks import update_course_notification


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        course_id = course.id
        course.last_update = timezone.now()

        update_course_notification.delay(course_id)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, ~IsModerator]

        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MaterialsPagination



class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]



class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    pagination_class = MaterialsPagination
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subscription_item = Subscription.objects.filter(user=user, course=course_item).first()

        if subscription_item:

            if subscription_item.status:
                subscription_item.status = False
                subscription_item.save()
                message = 'Вы отписались от курса.'
            else:
                subscription_item.status = True
                subscription_item.save()
                message = 'Вы подписались на курс.'
        else:
            Subscription.objects.create(course=course, user=user, status=True)
            message = 'подписка добавлена'

        return Response({'message': message})


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]