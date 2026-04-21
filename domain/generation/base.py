from abc import ABC, abstractmethod

class SongGeneratorStrategy(ABC):
    """Abstract base class for song generation strategies."""
    
    @abstractmethod
    def generate(self, song):
        """Initiates the generation process and returns a task reference."""
        pass

    @abstractmethod
    def check_status(self, song):
        """Checks the status of an ongoing generation task."""
        pass