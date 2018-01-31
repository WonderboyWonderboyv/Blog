from rest_framework.generics import (
	ListAPIView,
	DestroyAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,
	CreateAPIView,
	)
from rest_framework.permissions import(
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)
from posts.api.permissions import IsOwnerOrReadOnly
from comments.models import Comment
from .serializers import (
	CommentSerializer,
	CommentDetailSerializer,
	)
from rest_framework.filters import(
	SearchFilter,
	OrderingFilter,
	)
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from django.db.models import Q

# class PostCreateSerializer(CreateAPIView):
# 	queryset  = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer 
# 	permission_classes = [IsAuthenticated]
# 	def perform_create(self, serializer):
# 		serializer.save(user=self.request.user)

class CommentListAPIView(ListAPIView):
	serializer_class = CommentSerializer
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('content', 'user__first_name',)
	pagination_class = PostPageNumberPagination
	def get_queryset(self):
		queryset_list  = Comment.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
			Q(content__icontains=q)|
			Q(user__first_name__icontains=q)|
			Q(user__last_name__icontains=q)
			).distinct()
		return queryset_list

class CommentDetailAPIView(RetrieveAPIView):
	queryset  = Comment.objects.all()
	serializer_class = CommentDetailSerializer


# class PostUpdateAPIView(RetrieveUpdateAPIView):
# 	queryset  = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	lookup_field = 'slug'
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
# 	def perform_update(self, serializer):
# 		serializer.save(user=self.request.user)

# class PostDeleteAPIView(DestroyAPIView):
# 	queryset  = Post.objects.all()
# 	serializer_class = PostDetailSerializer
# 	lookup_field = 'slug'
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]