from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	)
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

class CommentSerializer(ModelSerializer):
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
		'id',
		'content_type',
		'object_id',
		'parent',
		'content',
		'reply_count',
		]
	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

class CommentChildSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Comment
		fields = [
		'user',
		'id',
		'content',
		'timestamp',
		]

class CommentDetailSerializer(ModelSerializer):
	reply_count = SerializerMethodField()
	replies = SerializerMethodField()
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Comment
		fields = [
		'id',
		'user',
		'content_type',
		'object_id',
		'parent',
		'content',
		'replies',
		'timestamp',
		]
	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None
	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0
