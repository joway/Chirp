from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


# Register your models here.

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = "__all__"

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"password\">this form</a>."
    )

    class Meta:
        model = User
        exclude = "__all__"

    def clean_password(self):
        return self.initial['password']


class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'is_activated', 'sex')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'name', 'sex', 'avatar')}),
        ('System Settings', {'fields': ('verification_code', 'subscribed')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_activated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'sex'),
        }),
    )
    ordering = ('-id',)
    search_fields = ('email', 'username')
    filter_horizontal = tuple()
    date_hierarchy = 'date_joined'


admin.site.register(User, UserAdmin)
