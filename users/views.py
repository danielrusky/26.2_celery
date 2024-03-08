from rest_framework import viewsets, generics

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from materials.permissions import IsOwner
from users.serializers import UserProfileSerializer, UserSerializer

from materials.models import Course


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsOwner]
        # if self.action in ['create']:
        #     permission_classes = [IsAdminUser]
        if self.action in ['create']:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = request.data.get('password')
        user = User.objects.get(email=serializer.data.get('email'))
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=201, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user == self.get_object() or self.request.user.is_superuser:
            serializer_class = UserSerializer
        else:
            serializer_class = UserProfileSerializer
        serializer = serializer_class(self.get_object())
        serializer_data = serializer.data
        return Response(serializer_data)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        user.payments = user.payment_set.all()
        return user


class PaymentCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, id=course_id)
        user = self.request.user

        if user.payment_set.filter(course=course).exists():
            raise serializers.ValidationError('У вас уже есть оплаченное обучение')
        serializer.save(user=user, course=course, amount=course.price)
