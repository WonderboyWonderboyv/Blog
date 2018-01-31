from .serializers import (
	UserCreateSerializer,
	UserLoginSerializer,
	)
from django.contrib.auth import get_user_model
from rest_framework.generics import (
	CreateAPIView,
	)
from rest_framework.permissions import(
	AllowAny,
	)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
User = get_user_model()

class UserCreateAPIView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer

class UserLoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer
	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)
