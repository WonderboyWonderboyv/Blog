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
from .permissions import IsOwnerOrReadOnly
from posts.models import Post
from .serializers import (
	PostListSerializer,
	PostDetailSerializer,
	PostCreateUpdateSerializer,
	)
from django.db.models import Q
from rest_framework.filters import(
	SearchFilter,
	OrderingFilter,
	)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


class PostCreateSerializer(CreateAPIView):
	queryset  = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer 
	permission_classes = [IsAuthenticated]
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'content', 'user__first_name',)
	pagination_class = PostPageNumberPagination
	def get_queryset(self):
		queryset_list  = Post.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
			Q(title__icontains=q)|
			Q(content__icontains=q)|
			Q(user__first_name__icontains=q)|
			Q(user__last_name__icontains=q)
			).distinct()
		return queryset_list

class PostDetailAPIView(RetrieveAPIView):
	queryset  = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset  = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
	queryset  = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]