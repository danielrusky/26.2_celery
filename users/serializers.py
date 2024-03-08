from rest_framework import serializers
# from materials.services import create_course_payment
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    course_payment_url = serializers.SerializerMethodField(read_only=True)

    # def get_course_payment_url(self, obj):
    #     if obj.course:
    #         if obj.course.price:
    #             stripe_response = create_course_payment(course=obj.course.title, price=int(obj.amount * 100))
    #             return stripe_response.url
    #         else:
    #             return 'У курса нет цены'
    #     else:
    #         return None

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payments_set', many=True, read_only=True)

    def create(self, validated_data):
        payment = validated_data.pop('payments_set', [])
        user = User.objects.create(**validated_data)

        for pay in payment:
            Payment.objects.create(user=user, **pay)
        return user

    class Meta:
        model = User
        fields = ['email']


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'city', 'avatar', 'payments']
