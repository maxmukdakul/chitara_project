from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    # Existing routes
    path('users/', views.create_user_api, name='create_user'),
    path('users/check/', views.check_user_api, name='check_user'),
    path('song-forms/', views.generate_song_api, name='generate_song'),
    path('song-forms/<int:song_id>/status/', views.check_song_status_api, name='check_song_status'),
    
    # New SRS required routes
    path('users/<int:user_id>/library/', views.get_library_api, name='get_library'),
    path('users/<int:user_id>/library/<int:song_id>/', views.delete_song_api, name='delete_song'),
    path('users/<int:user_id>/notifications/', views.get_notifications_api, name='get_notifications'),
    path('songs/shared/<int:song_id>/', views.share_song_api, name='share_song'),
]