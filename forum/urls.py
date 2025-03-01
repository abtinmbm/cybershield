from django.urls import path

# Change the import statement to specifically import the needed view functions
from .views import (
    signup,
    add_reply,
    login_view,
    terms_conditions,
    forum_list,
    create_forum,
    forum_list_json,
    logout_view,
    moderator_form,
    like_comment,
    delete_discussion,
    delete_comment,
    add_comment,
    view_discussion,
    user_profile,
    vote_post,
    vote_reply,
)

urlpatterns = [
    path("", forum_list, name="forum_list"),
    path("json/forum_list", forum_list_json, name="forum_list_json"),
    path("create_forum", create_forum, name="create_forum"),
    path("terms_conditions", terms_conditions, name="terms_conditions"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("user_signup", signup, name="signup"),
    path("become_moderator", moderator_form, name="moderator_form"),
    path("add_reply/", add_reply, name="add_reply"),
    path("comment/<int:comment_id>/like/", like_comment, name="like_comment"),
    path(
        "discussion/<int:discussion_id>/delete/",
        delete_discussion,
        name="delete_discussion",
    ),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path("discussion/<int:discussion_id>/comment/", add_comment, name="add_comment"),
    path("discussion/<int:discussion_id>/", view_discussion, name="view_discussion"),
    path("user/<str:username>/", user_profile, name="user_profile"),
    path('vote/post/', vote_post, name='vote_post'),
    path('vote/reply/', vote_reply, name='vote_reply'),
]
