from rest_framework.serializers import(
	ModelSerializer,
	EmailField,
	CharField,
	ValidationError,
	)
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
	email = EmailField(label='Email Address')
	email2 = EmailField(label='Confirm email')
	class Meta:
		model = User
		fields = [
		'username',
		'password',
		'email',
		'email2',
		]
		extra_kwargs = {
			'password': {'write_only': True}
		}
	def validate(self, data):
		email = data['email']
		user_qs = User.objects.filter(email=email)
		if user_qs.exists():
			raise ValidationError("This user is already registered.")
		return data
	def validate_email2(self, value):
		data = self.get_initial()
		email1 = data.get('email')
		email2 = value
		if email1 != email2:
			raise ValidationError("Emails must match.")
		user_qs = User.objects.filter(email=email2)
		if user_qs.exists():
			raise ValidationError("This user is already registered.")
		return value
	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_object = User(
			username = username,
			email = email,
			)
		user_object.set_password(password)
		user_object.save()
		return validated_data

class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
		'username',
		'first_name',
		'last_name',
		]

class UserLoginSerializer(ModelSerializer):
	token =CharField(allow_blank=True, read_only=True)
	username = CharField(required=False, allow_blank=True)
	email = EmailField(label='Email Address', required=False, allow_blank=True)
	class Meta:
		model = User
		fields = [
		'username',
		'password',
		'email',
		'token',
		]
		extra_kwargs = {
			'password': {'write_only': True}
		}
	def validate(self, data):
		email = data.get('email', None)
		username = data.get('username', None)
		user_obj = None
		if not email and not username:
			raise ValidationError('A username or an email is required to login.')
		user = User.objects.filter(
			Q(email=email)|
			Q(username=username)
			).distinct()
		user = user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count()==1:
			user_obj = user.first()
		else:
			raise ValidationError('This email/username is not valid.')

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError('Incorrect credentials.Please try again.')

		data['token'] = 'token'
		return data

