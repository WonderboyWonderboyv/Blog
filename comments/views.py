from django.shortcuts import render, get_object_or_404
from .models import Comment
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/login/')
def comment_detail(request, id):
	try:
		instance = Comment.objects.get(id=id)
	except:
		raise Http404
	# if not instance.is_parent:
	# 	instance = instance.parent
	content_object = instance.content_object
	content_id = instance.content_object.id
	initial_data={
		"content_type":instance.content_type,
		"object_id":instance.object_id,
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
	template = 'comment_detail.html'
	context = {'comment':instance , 'comment_form':comment_form}
	return render(request,template,context)

def comment_delete(request, id):
	#instance  = get_object_or_404(Comment, id=id)
	try:
		instance = Comment.objects.get(id=id)
	except:
		raise Http404
	if instance.user != request.user:
		# messages.error(request, "You don't have permission to delete it.")
		# raise Http404
		response = HttpResponse("You don't have permission to delete it.")
		response.status_code = 403
		return response
	if request.method == "POST":
		parent_url = instance.content_object.get_absolute_url()
		instance.delete()
		messages.success(request, "This has been deleted.")
		return HttpResponseRedirect(parent_url)
	template = 'confirm_delete.html'
	context = {'instance':instance}
	return render(request,template,context)