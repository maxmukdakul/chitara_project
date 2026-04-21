import requests
from django.conf import settings
from .base import SongGeneratorStrategy
from domain.models import GenerateStatus

class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    BASE_URL = "https://api.sunoapi.org/api/v1/generate"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {settings.SUNO_API_KEY}",
            "Content-Type": "application/json"
        }

    def generate(self, song):
        # 1. Create generation task
        payload = {
            "prompt": f"A {song.genre} song about {song.title}. Mood: {song.mood}. Occasion: {song.occasion}.",
            "instrumental": False, 
            "make_instrumental": False, 
            "wait_audio": False,
            "callBackUrl": "https://example.com/dummy-callback",
            "model": "V4_5",
            "customMode": False  # <--- Added customMode here!
        }
        
        response = requests.post(self.BASE_URL, json=payload, headers=self._get_headers())
        
        if response.status_code == 200:
            data = response.json()
            
            # Suno sometimes returns 200 HTTP OK, but an error code inside the JSON
            if data.get('code') == 200 and data.get('data'):
                song.task_id = data['data'].get('taskId')
                song.generation_status = GenerateStatus.PENDING
                song.save()
                return data
            else:
                song.generation_status = GenerateStatus.FAIL
                song.save()
                return {"error": data.get('msg', 'Suno API error')}
        else:
            song.generation_status = GenerateStatus.FAIL
            song.save()
            return {"error": "Failed to connect to Suno API"}

    def check_status(self, song):
        if not song.task_id:
            return {"error": "No task ID found for this song."}

        # 3. Check generation status via polling [cite: 473-475, 479]
        url = f"{self.BASE_URL}/record-info?taskId={song.task_id}"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            return response.json()
        return {"error": "Failed to fetch status"}