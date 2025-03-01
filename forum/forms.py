from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, ForumTag, ForumPost, Moderator
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    bio = forms.CharField(widget=forms.Textarea(), required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = CustomUser  # Changed from User to CustomUser
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if self.cleaned_data.get("bio"):
            user.bio = self.cleaned_data.get("bio")
            
        if self.cleaned_data.get("profile_pic"):
            user.profile_pic = self.cleaned_data.get("profile_pic")
        
        if commit:
            user.save()
            
        return user


class ModeratorCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm Password"
    )
    bio = forms.CharField(widget=forms.Textarea(), required=True)
    profile_pic = forms.ImageField(required=False)
    certifications = forms.CharField(
        required=True, help_text="List your relevant cybersecurity certifications"
    )
    agree_terms = forms.BooleanField(required=True)
    
    class Meta:
        model = Moderator
        # Exclude username field from automatic model field handling
        fields = ["email", "bio", "profile_pic", "certifications"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords don't match")

        bio = cleaned_data.get("bio")
        if bio and len(bio) < 100:
            self.add_error("bio", "Bio must be at least 100 characters")

        return cleaned_data

    def save(self, commit=True):
        # Create a new empty moderator instance without saving it
        moderator = super().save(commit=False)
        
        # Create a CustomUser directly (not a standard User)
        custom_user = CustomUser.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"]
        )
        
        # Now set the username field with the CustomUser instance
        moderator.username = custom_user
        moderator.Email = self.cleaned_data["email"]
        moderator.status = "pending"  # Set status to pending by default
        
        if self.cleaned_data.get("profile_pic"):
            moderator.profile_pic = self.cleaned_data["profile_pic"]
            
        if commit:
            moderator.save()
            
        return moderator


class CreateForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ["title", "content", "forum_tag"]  # Changed 'tags' to 'forum_tag'
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["forum_tag"].label = "Category"
        self.fields["forum_tag"].widget.attrs.update({"class": "form-select"})

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Get the CustomUser instance that corresponds to the authenticated user
        from forum.models import CustomUser

        # This gets the username from the request user and finds the corresponding CustomUser
        if hasattr(self, "user"):
            try:
                custom_user = CustomUser.objects.get(username=self.user.username)
                instance.author = custom_user
            except CustomUser.DoesNotExist:
                # Handle case where there is no matching CustomUser
                pass

        if commit:
            instance.save()
        return instance
