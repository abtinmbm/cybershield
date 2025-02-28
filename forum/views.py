import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import ForumPost, ForumReply, ForumTag, CustomUser, Moderator, Comment, Discussion
from .forms import UserCreationForm, ModeratorCreationForm, CreateForumPostForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .functions import get_public_resource_moderator, get_public_resource_user

# View to return the forum list in JSON format to be used for fitlering and searching
def forum_list(request):
    # Fetch public resources for users and moderators
    user_resources = get_public_resource_user()
    moderator_resources = get_public_resource_moderator()

    # Fetch all forum tags
    forum_tags = ForumTag.objects.all()
    
    # Fetch all forum posts
    forum_posts = ForumPost.objects.all().order_by('-created_at')

    # Render the forum list template with the fetched data
    return render(
        request,
        "forum_list.html",
        {
            "forum_tags": forum_tags,
            "forum_posts": forum_posts,  # Add this line to provide forum posts to the template
            "user_resources": user_resources,
            "user_resources_json": json.dumps(user_resources),
            "moderator_resources": moderator_resources,
            "moderator_resources_json": json.dumps(moderator_resources),
        },
    )

@login_required
def create_forum(request):
    if request.method == "POST":
        form = CreateForumPostForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save()
            return redirect('forum_list')
    else:
        form = CreateForumPostForm(user=request.user)
    
    return render(request, "create_forum.html", {"form": form})

def moderator_form(request):
    if request.method == "POST":
        form = ModeratorCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if user already exists
            if User.objects.filter(username__iexact=form.cleaned_data["username"]).exists():
                form.add_error("username", "Username already exists")
                return render(request, "moderator_form.html", {"form": form})
            if User.objects.filter(email__iexact=form.cleaned_data["email"]).exists():
                form.add_error("email", "Email already exists")
                return render(request, "moderator_form.html", {"form": form})

            try: 
                # Create a new moderator
                with transaction.atomic():
                    # Create the User first
                    user = form.save()
                    
                    # Log in the user
                    auth_login(request, authenticate(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password']
                    ))
                    
                    # Redirect to success page
                    return render(request, "moderator_success.html")
            
            except IntegrityError:
                form.add_error(None, "An error occurred during registration. Please try again.")
    else:
        form = ModeratorCreationForm()
    
    return render(request, "moderator_form.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if user already exists
            if User.objects.filter(username__iexact=form.cleaned_data["username"]).exists():
                form.add_error("username", "Username already exists")
                return render(request, "signup.html", {"form": form})
            
            if User.objects.filter(email__iexact=form.cleaned_data["email"]).exists():
                form.add_error("email", "Email already exists")
                return render(request, "signup.html", {"form": form})

            try:
                user = form.save()
                
                # Log the user in automatically after signing up
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
                if user is not None:
                    auth_login(request, user)
                
                return redirect('forum_list')
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = UserCreationForm()
    
    return render(request, "signup.html", {"form": form})

 # View to handle login page

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('forum_list')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password. Please try again.',
                'username': username  # Preserve the username so user doesn't have to retype
            })
            
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('forum_list')  # Redirect to home page after logout

# View to render the terms and conditions page
def terms_conditions(request):
    return render(request, "terms_conditions.html")

# View to handle forum creation form submission

# Add this view function for JSON API
def forum_list_json(request):
    # Fetch all forum posts
    posts = ForumPost.objects.all().order_by('-created_at')
    
    # Convert posts to JSON-serializable format
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'forum_tag': post.forum_tag.name,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'likes': post.likes.count(),
            'dislikes': post.dislikes.count(),
            'replies': ForumReply.objects.filter(post=post).count(),
        })
    
    return JsonResponse({'posts': posts_data})

@login_required
def add_reply(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        
        if post_id and content:
            try:
                post = ForumPost.objects.get(id=post_id)
                reply = ForumReply.objects.create(
                    content=content,
                    author=request.user,
                    post=post
                )
                
                return JsonResponse({
                    'status': 'success',
                    'author': request.user.username
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error', 
                    'message': str(e)
                }, status=400)
                
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def like_comment(request, comment_id):
    # Get the comment using ForumReply instead of Comment
    comment = get_object_or_404(ForumReply, id=comment_id)
    
    if request.user in comment.likes.all():
        # User already liked the comment, so unlike
        comment.likes.remove(request.user)
        liked = False
    else:
        # User hasn't liked the comment, so add like
        comment.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'success': True,
        'likes_count': comment.likes.count(),
        'liked': liked
    })

@login_required
def delete_discussion(request, discussion_id):
    # Get the discussion using ForumPost
    discussion = get_object_or_404(ForumPost, id=discussion_id)
    
    # Check if the user is the owner of the discussion
    if discussion.author != request.user:
        messages.error(request, "You don't have permission to delete this discussion.")
        return redirect('forum_list')
    
    # Delete the discussion
    discussion.delete()
    
    messages.success(request, "Discussion deleted successfully.")
    return redirect('forum_list')

@login_required
def delete_comment(request, comment_id):
    # Get the comment using ForumReply
    comment = get_object_or_404(ForumReply, id=comment_id)
    
    # Check if the user is the owner of the comment
    if comment.author != request.user:
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('forum_list')
    
    # Delete the comment
    comment.delete()
    
    messages.success(request, "Comment deleted successfully.")
    return redirect('forum_list')

@login_required
def delete_discussion(request, discussion_id):
    discussion = get_object_or_404(ForumPost, id=discussion_id)
    
    # Check if the user is the owner of the discussion
    if discussion.author != request.user:
        messages.error(request, "You don't have permission to delete this discussion.")
        return redirect('forum_list')
    
    # Delete the discussion
    discussion.delete()
    
    messages.success(request, "Discussion deleted successfully.")
    return redirect('forum_list')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the owner of the comment
    if comment.author != request.user:
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('view_discussion', discussion_id=comment.discussion.id)
    
    # Store the discussion ID before deleting the comment
    discussion_id = comment.discussion.id
    
    # Delete the comment
    comment.delete()
    
    messages.success(request, "Comment deleted successfully.")
    return redirect('view_discussion', discussion_id=discussion_id)

@login_required
def add_comment(request, discussion_id):
    discussion = get_object_or_404(ForumPost, id=discussion_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                content=content,
                author=request.user,
                discussion=discussion
            )
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Comment cannot be empty.")
    
    return redirect('view_discussion', discussion_id=discussion_id)

# Add a new view for displaying a specific discussion with its comments
@login_required
def view_discussion(request, discussion_id):
    discussion = get_object_or_404(ForumPost, id=discussion_id)
    comments = Comment.objects.filter(discussion=discussion).order_by('created_at')
    
    return render(request, 'discussion_detail.html', {
        'discussion': discussion,
        'comments': comments
    })