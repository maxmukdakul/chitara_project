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
        # 1. Build a powerful prompt including the voice type!
        prompt_text = f"{song.voice_type} vocals, {song.genre} style. A song about {song.title}. Mood: {song.mood}. Occasion: {song.occasion}."
        
        # 2. Add the optional story/lyrics if the user typed them
        if getattr(song, 'story_text', None):
            prompt_text += f" Story/Lyrics: {song.story_text}"

        # 3. Create generation task
        payload = {
            "prompt": prompt_text,
            "instrumental": False, 
            "make_instrumental": False, 
            "wait_audio": False,
            "callBackUrl": "https://example.com/dummy-callback",
            "model": "V4_5",
            "customMode": False
        }
        
        response = requests.post(self.BASE_URL, json=payload, headers=self._get_headers())
        
        print(f"Suno API POST response status: {response.status_code}")
        print(f"Suno API POST response text: {response.text}")
        
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
            return {"status": "error", "message": "No task ID"}

        url = f"{self.BASE_URL}/record-info?taskId={song.task_id}"
        response = requests.get(url, headers=self._get_headers())
        
        print(f"Suno API GET response status: {response.status_code}")
        print(f"Suno API GET response text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            # Extract status
            suno_status = data.get('data', {}).get('status')
            audio_url = None
            if suno_status == 'SUCCESS':
                suno_records = data.get('data', {}).get('response', {}).get('sunoData', [])
                if suno_records:
                    track = suno_records[0]
                    audio_url = track.get('audioUrl') or track.get('streamAudioUrl')
            return {
                "status": suno_status,
                "audio_url": audio_url,
                "task_id": song.task_id
            }
        return {"status": "error"}