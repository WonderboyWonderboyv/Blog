from urllib import quote_plus
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from .models import Post
from .forms import PostForm
from comments.models import Comment
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.forms import CommentForm
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		print form.cleaned_data.get('title')
		instance.save()
		messages.success(request, "Successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
		#print request.POST.get('content')
		#rint request.POST.get('title')
	else:
		messages.error(request, "Not successfully created")
	context = {'form':form}
	return render(request, 'post_form.html', context)

def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	#share_string = quote_plus(instance.content)
	initial_data={
		"content_type":instance.get_content_type,
		"object_id":instance.id,
	}
	comment_form = CommentForm(request.POST or None, initial=initial_data)
	if comment_form.is_valid() and request.user.is_authenticated():
		print(comment_form.cleaned_data)
		content_type_model = comment_form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=content_type_model)
		object_id = comment_form.cleaned_data.get("object_id")
		content = comment_form.cleaned_data.get("comment")
		parent_obj = None
		try:
			parent_id = request.POST.get("parent_id")
		except:
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count()==1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
			user = request.user,
			content_type = content_type,
			object_id = object_id,
			content = content,
			parent = parent_obj,
			)
		if created:
			print('it worked')
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments#Comment.objects.filter_by_instance(instance)
	context = {'title':instance.title, 'instance':instance, 'comments':comments,'comment_form':comment_form}#, 'share_string':share_string}
	return render(request, 'post_detail.html', context)

def post_list(request):
	today = timezone.now()
	queryset_list = Post.objects.active()#.order_by('-timestamp')
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()	
	title = 'List'
	q = request.GET.get('q')
	if q:
		queryset_list = queryset_list.filter(
			Q(title__icontains=q)|
			Q(content__icontains=q)|
			Q(user__first_name__icontains=q)|
			Q(user__last_name__icontains=q)
			).distinct()#no distinct posts
	paginator = Paginator(queryset_list, 5)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	context = {'queryset':queryset, 'title':title,'today':today}
	return render(request, 'post_list.html', context)
  
def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit = False)
		print form.cleaned_data.get('title')
		instance.save()
		messages.success(request, "Saved", extra_tags='some-tag')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {'form':form}
	return render(request, 'post_form.html', context)

def post_delete(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Deleted.")
	return redirect("posts:list")