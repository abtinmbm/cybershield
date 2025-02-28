from django import forms
from django.contrib.auth.models import User
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
        model = User
        fields = ['username', 'email']
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")
            
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            
            # Create a custom user profile
            custom_user = CustomUser.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio', ''),
                profile_pic=self.cleaned_data.get('profile_pic')
            )
            
        return user

class ModeratorCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    bio = forms.CharField(widget=forms.Textarea(), required=True)
    profile_pic = forms.ImageField(required=False)
    certifications = forms.CharField(required=True, help_text="List your relevant cybersecurity certifications")
    agree_terms = forms.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords don't match")
            
        bio = cleaned_data.get('bio')
        if bio and len(bio) < 100:
            self.add_error('bio', "Bio must be at least 100 characters")
            
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  # Moderators get staff status
        
        if commit:
            user.save()
            
            # Create a moderator profile
            moderator = Moderator.objects.create(
                user=user,
                bio=self.cleaned_data['bio'],
                profile_pic=self.cleaned_data.get('profile_pic'),
                certifications=self.cleaned_data['certifications'],
                forum_tag=self.cleaned_data['forum_tag']
            )
            
            # Add user to moderators group
            moderator_group, created = Group.objects.get_or_create(name='Moderators')
            moderator_group.user_set.add(user)
            
        return user
        
class CreateForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'forum_tag']  # Changed 'tags' to 'forum_tag'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['forum_tag'].label = "Category"
        self.fields['forum_tag'].widget.attrs.update({'class': 'form-select'})
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Get the CustomUser instance that corresponds to the authenticated user
        from forum.models import CustomUser
        
        # This gets the username from the request user and finds the corresponding CustomUser
        if hasattr(self, 'user'):
            try:
                custom_user = CustomUser.objects.get(username=self.user.username)
                instance.author = custom_user
            except CustomUser.DoesNotExist:
                # Handle case where there is no matching CustomUser
                pass
        
        if commit:
            instance.save()
        return instance