import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import (
    ForumPost,
    ForumReply,
    ForumTag,
    CustomUser,
    Moderator,
    Comment,
    Discussion,
)
from .forms import (
    UserCreationForm,
    ModeratorCreationForm,
    CreateForumPostForm,
    LoginForm,
)
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .functions import get_public_resource_moderator, get_public_resource_user
import logging

logger = logging.getLogger(__name__)


# View to return the forum list in JSON format to be used for fitlering and searching
def forum_list(request):
    # Fetch public resources for users and moderators
    user_resources = get_public_resource_user()
    moderator_resources = get_public_resource_moderator()

    # Fetch all forum tags
    forum_tags = ForumTag.objects.all()

    # Fetch all forum posts
    forum_posts = ForumPost.objects.all().order_by("-created_at")

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
            return redirect("forum_list")
    else:
        form = CreateForumPostForm(user=request.user)

    return render(request, "create_forum.html", {"form": form})


def moderator_form(request):
    if request.method == "POST":
        form = ModeratorCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if user already exists - using CustomUser instead of User
            if CustomUser.objects.filter(
                username__iexact=form.cleaned_data["username"]
            ).exists():
                form.add_error("username", "Username already exists")
                return render(request, "moderator_form.html", {"form": form})

            if CustomUser.objects.filter(
                email__iexact=form.cleaned_data["email"]
            ).exists():
                form.add_error("email", "Email already exists")
                return render(request, "moderator_form.html", {"form": form})

            try:
                # Create a new moderator with pending status
                with transaction.atomic():
                    moderator = form.save()

                    # Redirect to success page - DO NOT log in the user
                    return render(request, "moderator_success.html")

            except IntegrityError:
                form.add_error(
                    None, "An error occurred during registration. Please try again."
                )
    else:
        form = ModeratorCreationForm()

    return render(request, "moderator_form.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Also update this check to use CustomUser
            if CustomUser.objects.filter(
                username__iexact=form.cleaned_data["username"]
            ).exists():
                form.add_error("username", "Username already exists")
                return render(request, "signup.html", {"form": form})

            if CustomUser.objects.filter(
                email__iexact=form.cleaned_data["email"]
            ).exists():
                form.add_error("email", "Email already exists")
                return render(request, "signup.html", {"form": form})

            try:
                user = form.save()

                # Log the user in automatically after signing up
                user = authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],
                )
                if user is not None:
                    auth_login(request, user)

                return redirect("forum_list")
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


# View to handle login page
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:
                # Check if the user has a pending or suspended moderator account
                try:
                    moderator = Moderator.objects.get(username=user)
                    if moderator.status == "pending":
                        form.add_error(
                            None,
                            "Your moderator application is pending approval. You'll receive an email when it's approved.",
                        )
                        return render(request, "login.html", {"form": form})
                    elif moderator.status == "suspended":
                        form.add_error(
                            None,
                            "Your moderator account has been suspended. Please contact the administration for more information.",
                        )
                        return render(request, "login.html", {"form": form})
                except Moderator.DoesNotExist:
                    # Not a moderator, proceed with login
                    pass

                auth_login(request, user)
                return redirect("forum_list")
            else:
                form.add_error(None, "Invalid username or password. Please try again.")

        # If form is not valid or authentication failed
        return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("forum_list")  # Redirect to home page after logout


# View to render the terms and conditions page
def terms_conditions(request):
    return render(request, "terms_conditions.html")


# View to handle forum creation form submission


# ...existing imports and code...


@login_required
def add_reply(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        content = request.POST.get("content")

        # Debug logging
        logger.debug(
            f"Received add_reply request - post_id: {post_id}, content: {content}"
        )

        if not post_id:
            return JsonResponse(
                {"status": "error", "message": "Missing post_id"}, status=400
            )

        if not content or not content.strip():
            return JsonResponse(
                {"status": "error", "message": "Content cannot be empty"}, status=400
            )

        try:
            # Get the post
            post = ForumPost.objects.get(id=post_id)

            # Create the reply
            reply = ForumReply.objects.create(
                post=post, author=request.user, content=content.strip()
            )

            # Return success response
            return JsonResponse(
                {
                    "status": "success",
                    "author": request.user.username,
                    "reply_id": reply.id,
                    "content": content,
                    "created_at": reply.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        except ForumPost.DoesNotExist:
            logger.error(f"Post not found with ID: {post_id}")
            return JsonResponse(
                {"status": "error", "message": "Post not found"}, status=404
            )
        except Exception as e:
            logger.error(f"Error creating reply: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=400
    )


# ...rest of existing code...


# Add this view function for JSON API
def forum_list_json(request):
    # Fetch all forum posts
    posts = ForumPost.objects.all().order_by("-created_at")

    # Convert posts to JSON-serializable format
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": post.author.username,
                "forum_tag": post.forum_tag.name,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "likes": post.likes.count(),
                "dislikes": post.dislikes.count(),
                "replies": ForumReply.objects.filter(post=post).count(),
            }
        )

    return JsonResponse({"posts": posts_data})


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

    return JsonResponse(
        {"success": True, "likes_count": comment.likes.count(), "liked": liked}
    )


@login_required
def delete_discussion(request, discussion_id):
    discussion = get_object_or_404(ForumPost, id=discussion_id)

    # Check if the user is the owner of the discussion, a moderator, or is staff
    if (
        discussion.author == request.user
        or request.user.role == "moderator"
        or request.user.is_staff
    ):
        discussion.delete()
        messages.success(request, "Discussion deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this discussion.")

    # Always redirect back to forum list
    return redirect("forum_list")


@login_required
def delete_comment(request, comment_id):
    # Try to get the comment from ForumReply
    comment = get_object_or_404(ForumReply, id=comment_id)
    parent_post = comment.post

    # Check if the user is the owner of the comment, a moderator, or is staff
    if (
        comment.author == request.user
        or request.user.role == "moderator"
        or request.user.is_staff
    ):
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this comment.")

    # If we came from the discussion detail page, go back there
    referer = request.META.get("HTTP_REFERER", "")
    if f"/discussion/{parent_post.id}" in referer:
        return redirect("view_discussion", discussion_id=parent_post.id)

    # Otherwise go back to forum list
    return redirect("forum_list")


@login_required
def add_comment(request, discussion_id):
    discussion = get_object_or_404(ForumPost, id=discussion_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                content=content, author=request.user, discussion=discussion
            )
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Comment cannot be empty.")

    return redirect("view_discussion", discussion_id=discussion_id)


# Add a new view for displaying a specific discussion with its comments
def view_discussion(request, discussion_id):
    # Get the discussion object or return 404 if not found
    discussion = get_object_or_404(ForumPost, id=discussion_id)

    # Get comments/replies for this post
    replies = ForumReply.objects.filter(post=discussion).order_by("created_at")

    # Add a context variable to identify if user is authenticated (for templates to use)
    context = {
        "discussion": discussion,
        "replies": replies,
        "is_authenticated": request.user.is_authenticated,
    }

    # Render the discussion detail template with context data
    return render(request, "discussion_detail.html", context)


# View user profile
def user_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    # Determine if user is a moderator
    is_moderator = profile_user.role == "moderator"

    # Get user's profile picture
    profile_pic = settings.MEDIA_URL + "DefaultPFP.jpg"
    moderator_data = None

    if is_moderator:
        # Get moderator data if user is a moderator
        try:
            moderator = Moderator.objects.get(username=profile_user)
            if moderator.profile_pic and hasattr(moderator.profile_pic, "url"):
                profile_pic = moderator.profile_pic.url
            moderator_data = {
                "bio": moderator.bio,
                "email": moderator.Email,
                "certifications": (
                    moderator.certifications
                    if hasattr(moderator, "certifications")
                    else None
                ),
            }
        except Moderator.DoesNotExist:
            pass

    # Get user's posts and replies
    all_user_posts = ForumPost.objects.filter(author=profile_user).order_by(
        "-created_at"
    )
    user_replies = ForumReply.objects.filter(author=profile_user).order_by(
        "-created_at"
    )[:5]

    # Calculate total likes received
    total_likes = 0
    for post in all_user_posts:
        total_likes += post.likes.count()

    for reply in ForumReply.objects.filter(author=profile_user):
        total_likes += reply.likes.count()

    # Get post count before slicing
    post_count = all_user_posts.count()

    # Determine if we should show "view all" button (if more than 5 posts)
    show_all_posts_button = post_count > 5

    # Limit posts for display
    user_posts = all_user_posts[:5]

    context = {
        "profile_user": profile_user,
        "is_moderator": is_moderator,
        "profile_pic": profile_pic,
        "moderator_data": moderator_data,
        "user_posts": user_posts,
        "post_count": post_count,  # Pass the post count separately
        "user_replies": user_replies,
        "total_likes": total_likes,
        "show_all_posts_button": show_all_posts_button,
    }

    return render(request, "user_profile.html", context)


@login_required
def vote_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        vote_type = request.POST.get("vote_type")

        try:
            post = ForumPost.objects.get(id=post_id)

            # Handle upvote
            if vote_type == "upvote":
                if request.user in post.likes.all():
                    post.likes.remove(request.user)
                    action = "removed"
                else:
                    post.likes.add(request.user)
                    post.dislikes.remove(request.user)  # Remove dislike if exists
                    action = "added"

            # Handle downvote
            elif vote_type == "downvote":
                if request.user in post.dislikes.all():
                    post.dislikes.remove(request.user)
                    action = "removed"
                else:
                    post.dislikes.add(request.user)
                    post.likes.remove(request.user)  # Remove like if exists
                    action = "added"

            return JsonResponse(
                {
                    "status": "success",
                    "likes_count": post.likes.count(),
                    "dislikes_count": post.dislikes.count(),
                    "action": action,
                    "vote_type": vote_type,
                }
            )

        except ForumPost.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Post not found"}, status=404
            )

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
def vote_reply(request):
    if request.method == "POST":
        reply_id = request.POST.get("reply_id")
        vote_type = request.POST.get("vote_type")

        try:
            reply = ForumReply.objects.get(id=reply_id)

            # Handle upvote
            if vote_type == "upvote":
                if request.user in reply.likes.all():
                    reply.likes.remove(request.user)
                    action = "removed"
                else:
                    reply.likes.add(request.user)
                    reply.dislikes.remove(request.user)  # Remove dislike if exists
                    action = "added"

            # Handle downvote
            elif vote_type == "downvote":
                if request.user in reply.dislikes.all():
                    reply.dislikes.remove(request.user)
                    action = "removed"
                else:
                    reply.dislikes.add(request.user)
                    reply.likes.remove(request.user)  # Remove like if exists
                    action = "added"

            return JsonResponse(
                {
                    "status": "success",
                    "likes_count": reply.likes.count(),
                    "dislikes_count": reply.dislikes.count(),
                    "action": action,
                    "vote_type": vote_type,
                }
            )

        except ForumReply.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Reply not found"}, status=404
            )

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser, ForumPost


# User profile view
def user_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    # Get user's posts and activity
    all_user_posts = ForumPost.objects.filter(author=profile_user).order_by(
        "-created_at"
    )
    user_replies = ForumReply.objects.filter(author=profile_user).order_by(
        "-created_at"
    )[:5]

    # Calculate total likes received
    total_likes = 0
    for post in all_user_posts:
        total_likes += post.likes.count()

    for reply in ForumReply.objects.filter(author=profile_user):
        total_likes += reply.likes.count()

    # Get post count before slicing
    post_count = all_user_posts.count()

    # Determine if we should show "view all" button (if more than 5 posts)
    show_all_posts_button = post_count > 5

    # Limit posts for display
    user_posts = all_user_posts[:5]

    return render(
        request,
        "user_profile.html",
        {
            "profile_user": profile_user,
            "user_posts": user_posts,
            "post_count": post_count,  # Pass the post count separately
            "user_replies": user_replies,
            "total_likes": total_likes,
            "show_all_posts_button": show_all_posts_button,
        },
    )


# Edit profile view
@login_required
def edit_profile(request):
    if request.method == "POST":
        bio = request.POST.get("bio", "")
        profile_pic = request.FILES.get("profile_picture", None)

        user = request.user
        user.bio = bio

        if profile_pic:
            user.profile_picture = profile_pic

        user.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect("user_profile", username=user.username)

    return render(request, "edit_profile.html")


# Change password view
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect("user_profile", username=user.username)
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "change_password.html", {"form": form})


# New view function for leaderboard
def leaderboard(request):
    # Get all users
    users = CustomUser.objects.all()
    
    # Calculate likes for each user
    user_stats = []
    for user in users:
        # Get likes from posts
        post_likes = sum(post.likes.count() for post in ForumPost.objects.filter(author=user))
        
        # Get likes from replies
        reply_likes = sum(reply.likes.count() for reply in ForumReply.objects.filter(author=user))
        
        # Total likes
        total_likes = post_likes + reply_likes
        
        # Add to user stats if they have any likes or posts
        if total_likes > 0 or ForumPost.objects.filter(author=user).exists():
            user_stats.append({
                'user': user,
                'post_likes': post_likes,
                'reply_likes': reply_likes,
                'total_likes': total_likes,
                'post_count': ForumPost.objects.filter(author=user).count(),
            })
    
    # Sort by total likes (descending)
    user_stats.sort(key=lambda x: x['total_likes'], reverse=True)
    
    # Add rank to each user
    for i, stats in enumerate(user_stats):
        stats['rank'] = i + 1
    
    return render(request, 'leaderboard.html', {
        'user_stats': user_stats[:20],  # Top 20 users
        'total_users': len(user_stats)
    })
