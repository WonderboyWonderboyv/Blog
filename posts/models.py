from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		#Post.objects.all() = super(PostManager,self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
def upload_location(instance,filename):
	print "%s/%s" %(instance.pk, filename)
	return "%s/%s" %(instance.pk, filename)
class Post(models.Model):
	title = models.CharField(max_length=30)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	#image = models.FileField(null=True, blank=True)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field='width_field', height_field='height_field')
	width_field = models.IntegerField(default=0)
	height_field = models.IntegerField(default=0)
	#updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)


	objects = PostManager()


	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		#return "/posts/%s/" %(self.id)
		#return reverse('posts:detail', kwargs={'id':self.id})
		return reverse('posts:detail', kwargs={'slug':self.slug})
	class Meta:
		ordering = ['-timestamp']

	def get_markdown(self):
		content = self.content
		marked_content = markdown(content)
		marked_content_safe =mark_safe(marked_content )
		return marked_content_safe

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs



def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug
def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)