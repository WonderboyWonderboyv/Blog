from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	)
from posts.models import Post
from comments.api.serializers import CommentSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

post_detail_url = HyperlinkedIdentityField(
	view_name = 'posts_api:detail',
	lookup_field = 'slug'
	)

class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
		'title',
		'content',
		'publish',
		]

class PostListSerializer(ModelSerializer):
	url = post_detail_url
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Post
		fields = [
		'url',
		'user',
		'title',
		'content',
		'publish',
		]
	# def get_user(self, obj):
	# 	return str(obj.user.username)

class PostDetailSerializer(ModelSerializer):
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Post
		fields = [
		'id',
		'user',
		'title',
		'slug',
		'content',
		'html',
		'publish',
		'image',
		'comments',
		]
	def get_html(self, obj):
		return obj.get_markdown()
	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image
	def get_comments(self, obj):
		comments_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentSerializer(comments_qs, many=True).data
		return comments