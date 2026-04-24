from django.urls import path
from . import views

urlpatterns = [
    # The URL to create a user
    path('api/users/', views.create_user_api, name='create_user_api'),
    # The URL to generate a song
    path('api/song-forms/', views.generate_song_api, name='generate_song_api'),
    # The URL to check if the song is finished
    path('api/song-forms/<int:song_id>/status/', views.check_song_status_api, name='check_song_status_api'),
]