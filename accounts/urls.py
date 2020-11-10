from django.urls import include, path

from .views import GithubLogin


urlpatterns = [
    path('', include('allauth.urls')),
    path('dj-rest-auth/github/', GithubLogin.as_view(), name='github-login'),
]
