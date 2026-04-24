import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.models import Song, User
from domain.generation.factory import get_generator_strategy

# --- 1. Endpoint to Create a User ---
@csrf_exempt
def create_user_api(request):
    """API to create a new user via Postman"""
    if request.method == 'POST':
        try:
            # Read the JSON data sent from Postman
            body = json.loads(request.body)
            
            # Create the user in the database
            # We use .get() so it doesn't crash if they forget to send a name
            user = User.objects.create(
                name=body.get('name', 'Anonymous User')
            )
            
            return JsonResponse({
                "message": "User created successfully",
                "user_id": user.id,
                "name": user.name
            }, status=201)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({'error': 'Please use POST method'}, status=405)


# --- 2. Endpoint to Generate a Song ---
@csrf_exempt
def generate_song_api(request):
    """API to trigger Suno generation via Postman"""
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            
            # Find the user by the ID sent in Postman
            user_id = body.get('user_id')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": f"User with ID {user_id} not found. Create a user first!"}, status=404)

            # Create a pending song using the data from Postman
            song = Song.objects.create(
                user=user, 
                title=body.get('title', 'Untitled Song'), 
                genre=body.get('genre', 'Pop'), 
                mood=body.get('mood', 'Happy'), 
                occasion=body.get('occasion', 'Casual')
            )
            
            # Trigger the strategy (Mock or Suno)
            generator = get_generator_strategy()
            result = generator.generate(song)
            
            # Return the exact format the TA expects
            return JsonResponse({
                'song_id': song.id,
                'title': song.title,
                'status': 'pending',
                'strategy_result': result
            }, status=200)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Please use POST method'}, status=405)

@csrf_exempt
def check_song_status_api(request, song_id):
    """API to poll the status of a generating song"""
    if request.method == 'GET':
        try:
            # 1. Find the song in the database using the ID from the URL
            try:
                song = Song.objects.get(id=song_id)
            except Song.DoesNotExist:
                return JsonResponse({"error": f"Song with ID {song_id} not found."}, status=404)

            # 2. Check if it even has a task ID
            if not song.task_id:
                return JsonResponse({"error": "This song does not have a generation task ID."}, status=400)

            # 3. Use the strategy to poll the API for the latest status
            generator = get_generator_strategy()
            result = generator.check_status(song)

            # 4. Return the result to Postman
            return JsonResponse({
                "song_id": song.id,
                "title": song.title,
                "database_status": song.generation_status,
                "suno_api_response": result
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Please use GET method'}, status=405)