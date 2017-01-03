from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from haystack.forms import SearchForm
# import qiniu
def full_search(request):
	"""全局搜索"""
	keywords = request.GET['q']
	sform = SearchForm(request.GET)
	posts = sform.search()
	print(posts)
	return render(request, 'blog/post_search_list.html',{'test': sform, 'posts': posts, 'list_header': '关键字 \'{}\' 搜索结果'.format(keywords)})

# Create your views here.
def post_list(request):
	postsAll=Post.objects.filter(published_date__isnull=False).order_by('-published_date')
	paginator=Paginator(postsAll,1)
	page=request.GET.get('page')
	try:	
	   posts = paginator.page(page)
	except PageNotAnInteger:	
	# If page is not an integer, deliver first page.	
	   posts = paginator.page(1)
	except EmptyPage:	
	# If page is out of range (e.g. 9999), deliver last page of results.	
	   posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})

def post_detail(request,pk):
	post=get_object_or_404(Post,pk=pk)
	return render(request,'blog/post_detail.html',{ 'post': post })

@login_required
def post_new(request):
	if request.method=="POST":
		form=PostForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form=PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
	   form = PostForm(request.POST, instance=post)
	if form.is_valid():
	   post = form.save(commit=False)
	   post.author = request.user
	   post.save()
	   return redirect('post_detail', pk=post.pk)
	else:
	   form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')