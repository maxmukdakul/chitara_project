from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from domain.models.song import Song
from domain.models.user import User
from domain.models.notification import Notification
from domain.models.choices.notification_type import NotificationType
from domain.generation.factory import get_generator_strategy

# --- 1. Endpoint to Create a User ---
@csrf_exempt
def create_user_api(request):
    """API to create a new user via Postman"""
    if request.method == 'POST':
        try:
            # Read the JSON data sent from Postman
            body = json.loads(request.body)
            
            # Extract data with safe fallbacks
            email = body.get('email', 'test@example.com')
            name = body.get('name', 'Testing User')
            
            # Use get_or_create to prevent crashes on duplicate emails!
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'name': name}
            )
            
            return JsonResponse({
                "message": "User created successfully" if created else "User already exists",
                "user_id": user.id,
                "name": user.name,
                "email": user.email
            }, status=201 if created else 200)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Please use POST method'}, status=405)

@csrf_exempt
def generate_song_api(request):
    """Creates a song and triggers the strategy pattern"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data.get('user_id'))
            
            # We are now catching ALL the fields from the frontend!
            song = Song.objects.create(
                user=user,
                title=data.get('title'),
                occasion=data.get('occasion'),
                genre=data.get('genre'),
                mood=data.get('mood'),
                voice_type=data.get('voice_type', 'Male'), # Catch voice
                story_text=data.get('story_text', ''),     # Catch story
                generation_status='Pending'
            )
            
            # Import and run your factory
            strategy = get_generator_strategy()
            result = strategy.generate(song)
            
            print(f"Generation result: {result}")
            
            return JsonResponse({'song_id': song.id, 'status': 'pending', 'task': result}, status=200)
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def check_song_status_api(request, song_id):
    """API to poll the status of a generating song and save metadata when done"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Please use GET method'}, status=405)

    try:
        # 1. Find the song
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return JsonResponse({"error": f"Song {song_id} not found."}, status=404)

        if not song.task_id:
            return JsonResponse({"error": "No task ID found."}, status=400)

        # 2. Get Strategy (Import inside the function to avoid circular errors)
        from domain.generation.factory import get_generator_strategy
        generator = get_generator_strategy()
        
        print(f"--- Polling Suno for Task: {song.task_id} ---")
        result = generator.check_status(song)
        
        print(f"Check status result: {result}")
        
        # 3. Extract status from the standardized response
        status = result.get('status')
        audio_url = result.get('audio_url')
        image_url = result.get('image_url')
        print(f"Current status: {status}")

        if status == 'SUCCESS':
            song.audio_url = audio_url
            song.image_url = image_url
            song.generation_status = 'Success'
            song.save()
            # Create notification
            Notification.objects.create(
                user=song.user,
                action_type=NotificationType.CREATED_SUCCESS,
                message=f"Song '{song.title}' generated successfully."
            )
            print(f"Successfully saved song {song.id} audio URL!")
        
        elif status in ['FAILED', 'REJECTED', 'GENERATE_AUDIO_FAILED']:
            song.generation_status = 'Fail'
            song.save()
            # Create notification
            Notification.objects.create(
                user=song.user,
                action_type=NotificationType.CREATED_FAIL,
                message=f"Song '{song.title}' generation failed."
            )

        # 4. Return clear JSON to the frontend
        return JsonResponse({
            "song_id": song.id,
            "status": song.generation_status,
            "audio_url": song.audio_url,
            "raw_api": result
        }, status=200)

    except Exception as e:
        print(f"Error in Status Check: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

# --- 1. Get User Library ---
@csrf_exempt
def get_library_api(request, user_id):
    """Returns all songs for a user, sorted newest first"""
    if request.method == 'GET':
        songs = Song.objects.filter(user_id=user_id).order_by('-created_at')
        song_list = [{
            "id": s.id,
            "title": s.title,
            "status": s.generation_status,
            "duration": str(s.duration_time) if s.duration_time else None,
            "audio_url": s.audio_url,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for s in songs]
        return JsonResponse({"library": song_list}, status=200)
    return JsonResponse({'error': 'GET method required'}, status=405)

# --- 2. Delete Song ---
@csrf_exempt
def delete_song_api(request, user_id, song_id):
    """Deletes a song and logs the notification"""
    if request.method == 'DELETE':
        try:
            song = Song.objects.get(id=song_id, user_id=user_id)
            title = song.title
            song.delete()
            
            # Create notification
            Notification.objects.create(
                user_id=user_id,
                action_type=NotificationType.DELETED,
                message=f"Deleted song: {title}"
            )
            return JsonResponse({"message": "Song deleted successfully"}, status=200)
        except Song.DoesNotExist:
            return JsonResponse({"error": "Song not found or you don't own it"}, status=404)
    return JsonResponse({'error': 'DELETE method required'}, status=405)

# --- 3. Share/View Song ---
@csrf_exempt
def share_song_api(request, song_id):
    """Allows anyone to view a song (no user_id required)"""
    if request.method == 'GET':
        try:
            song = Song.objects.get(id=song_id)
            
            # Log share notification for the owner
            Notification.objects.create(
                user_id=song.user.id,
                action_type=NotificationType.SHARED,
                message=f"Song link accessed: {song.title}"
            )
            
            return render(request, 'domain/song_detail.html', {
                'song': song,
                'user': None,
                'shared_link': None
            })
        except Song.DoesNotExist:
            return HttpResponse("Song not found", status=404)
    return JsonResponse({'error': 'GET method required'}, status=405)

def song_detail(request, song_id):
    """View song details for owners"""
    try:
        song = Song.objects.get(id=song_id)
        user = request.session.get('user')
        if user and song.user.id == user['user_id']:
            shared_link = f"{request.scheme}://{request.get_host()}/songs/shared/{song.id}/"
            return render(request, 'domain/song_detail.html', {
                'song': song,
                'user': user,
                'shared_link': shared_link
            })
        else:
            return redirect(f'/songs/shared/{song.id}/')
    except Song.DoesNotExist:
        return HttpResponse("Song not found", status=404)

# --- 4. Get Notifications History ---
@csrf_exempt
def get_notifications_api(request, user_id):
    """Returns the action history for a user"""
    if request.method == 'GET':
        notifications = Notification.objects.filter(user_id=user_id).order_by('-timestamp')
        history = [{
            "action": n.action_type,
            "message": n.message,
            "time": n.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for n in notifications]
        return JsonResponse({"history": history}, status=200)
    return JsonResponse({'error': 'GET method required'}, status=405)

def index_view(request):
    """Serves the main frontend UI"""
    return render(request, 'domain/index.html')

# --- 5. Check if User Exists ---
@csrf_exempt
def check_user_api(request):
    """Checks if an email is already in the database before logging in"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            # Try to find the user
            user = User.objects.get(email=email)
            
            # If found, return their data
            return JsonResponse({
                "exists": True, 
                "user_id": user.id, 
                "name": user.name, 
                "email": user.email
            }, status=200)
            
        except User.DoesNotExist:
            # If not found, tell the frontend they are new
            return JsonResponse({"exists": False}, status=200)
            
    return JsonResponse({'error': 'POST method required'}, status=405)