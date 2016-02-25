from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import *
from django.http import HttpResponse, Http404
from mimetypes import guess_type

@login_required
def global_post(request):
	posts = Post.objects.all().order_by('-post_time')
	follow_posts = Follow.objects.get(user = request.user).follow_posts.all()
	context = {
		'posts' : posts[0:15],
		'follow_posts': follow_posts,
	}
	return render(request, 'socialnetwork/global.html', context)
#
@login_required	
def profile(request):
	context = {}
	posts = Post.objects.filter(user = request.user).order_by('-post_time')
	self_info = get_object_or_404(Entry, user = request.user)
	name = request.user.username
	context = {
		'posts' : posts[0:15],
		'self_info' : self_info,
		'name' : name,
	}	
	return render(request, 'socialnetwork/profile.html', context)

@login_required
@transaction.atomic
def delete_post(request, id):
	errors = []
	try:
		post_to_delete = Post.objects.get(id = id, user = request.user)
		comments_to_delete = Comment.objects.filter(post = post_to_delete)
		comments_to_delete.delete()
		post_to_delete.delete()
		
	except ObjectDoesNotExist:
		errors.append('The post did not exist')
	return redirect('profile')
	
@login_required
def other_profile(request, name):
	user = User.objects.filter(username = name)
	posts = Post.objects.filter(user = user).order_by('-post_time')
	other_info = Entry.objects.get(user = user)
	context = {
		'name' : name,
		'posts' : posts[0:15],
		'other_info' : other_info,
	}
	return render(request, 'socialnetwork/other_profile.html', context)
	
@login_required
def do_post(request):
	errors = []
	#create a new post
	if not 'post' in request.POST or not request.POST['post']:
		errors.append('You must tap in something to post')
	elif len(request.POST['post']) > 420:
		errors.append('Your infomation has exceed the length limitation 420')
	else:		
		postInfo = request.POST['post']	
		check_string = ""
		for i in range(0, len(postInfo)):
			check_string += " "
		if(check_string == postInfo) or postInfo == "\t":
			errors.append('You must tap in something to post')
		else:
			new_post = Post(text = request.POST['post'], user = request.user)
			new_post.save()
	context = {}
	posts = Post.objects.filter(user = request.user).order_by('-post_time')
	self_info = get_object_or_404(Entry, user = request.user)
	name = request.user.username
	context = {
		'posts' : posts[0:15],
		'self_info' : self_info,
		'name' : name,
		'errors' : errors,
	}	
	return render(request, 'socialnetwork/profile.html', context)

@login_required
def do_comment(request):
	errors = []
	if not 'post' in request.POST or not request.POST['comment']:
		errors.append('You must tap in something to post')
	else:
		post_id = request.POST['post']
		post = Post.objects.get(pk = post_id)
		new_comment = Comment(post = post,
							  text = request.POST['comment'],
							  comment_person = request.user.username,
							)
		new_comment.save()
	return HttpResponse("comment success");
	
@transaction.atomic
def register(request):
	context = {}
	
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'socialnetwork/register.html', context)
	
	form = RegistrationForm(request.POST)
	context['form'] = form
	
	if not form.is_valid():
		return render(request, 'socialnetwork/register.html', context)
	
	new_user = User.objects.create_user(username=form.cleaned_data['username'],  
                                       password=form.cleaned_data['password1']) 
	new_user.save()
	
	follow = Follow.objects.create(user = new_user)
	follow.save()
	
	new_user = authenticate(username=form.cleaned_data['username'],  
                            password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect('edit')

@login_required
def add_entry(request):
	context = {}
	if request.method == 'GET':
		context['form'] = EntryForm()
		return render(request, 'socialnetwork/edit.html', context)
	entry = Entry(user = request.user)
	form = EntryForm(request.POST, request.FILES, instance = entry)
	context['form'] = form
	form.save()
	return redirect('profile')
	
@login_required
def edit_entry(request):
	context = {}
	if request.method == "GET":
		context['form'] = EntryForm()
		return render(request, 'socialnetwork/edit.html', context)
		
	new_entry = Entry(user = request.user)
	form = EntryForm(request.POST, request.FILES, instance = new_entry)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'socialnetwork/edit.html', context)
	form.save()
	return redirect('profile')

@login_required
def get_photo(request, name):
	user = User.objects.get(username = name)
	entry = get_object_or_404(Entry, user = user)
	if not entry.photo:
		raise Http404
	content_type = guess_type(entry.photo.name)
	return HttpResponse(entry.photo, content_type = content_type)

@login_required
def follow_users(request, name):
	user = request.user
	follow = Follow.objects.get(user = user)
	follow_user = User.objects.get(username = name)
	posts = Post.objects.filter(user = follow_user)
	for post in posts:
		follow.follow_posts.add(post)
	follow.save()
	follow_posts = follow.follow_posts.all()
	context = {
		'follow_posts' : follow_posts,
	}
	return redirect('global_post')

@login_required
def follow_delete(request, name):
	user = request.user
	follow = Follow.objects.get(user = user)
	unfollow_user = User.objects.get(username = name)
	posts_delete = Post.objects.filter(user = unfollow_user)
	for post in posts_delete:
		follow.follow_posts.remove(post)
	follow.save()
	return redirect('global_post')
	
@login_required
def follow_stream(request):
	follow_posts = Follow.objects.get(user = request.user).follow_posts.all().order_by('-post_time')
	context = {
		'follow_posts' : follow_posts
	}
	return render(request, "socialnetwork/follow.html", context)

@login_required	
def post_list(request):
	follow_posts = Follow.objects.get(user = request.user).follow_posts.all()
	posts = Post.objects.all().order_by('-post_time')
	context = {
		'posts' : posts[0:15],
		'follow_posts': follow_posts,
	}
	return render(request, 'socialnetwork/posts.xml', context, content_type='application/xml')

@login_required
def comment_list(request, post_id):
	post = Post.objects.get(pk = post_id)
	comments = Comment.objects.filter(post = post).order_by('comment_time')
	context = {
		'comments' : comments,
	}
	return render(request, 'socialnetwork/comments.xml', context, content_type='application/xml')

	
	