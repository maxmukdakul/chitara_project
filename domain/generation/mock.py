import uuid
from .base import SongGeneratorStrategy
from domain.models import GenerateStatus

class MockSongGeneratorStrategy(SongGeneratorStrategy):
    def generate(self, song):
        # Produces predictable offline output
        song.task_id = f"mock_task_{uuid.uuid4().hex[:8]}"
        song.generation_status = GenerateStatus.SUCCESS
        song.shared_link = f"https://mock-audio.local/{song.task_id}.mp3"
        song.save()
        
        return {
            "status": "success",
            "message": "Mock generation completed instantly.",
            "task_id": song.task_id
        }

    def check_status(self, song):
        return {
            "status": GenerateStatus.SUCCESS,
            "task_id": song.task_id
        }