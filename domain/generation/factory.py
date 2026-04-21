from django.conf import settings
from .mock import MockSongGeneratorStrategy
from .suno import SunoSongGeneratorStrategy

def get_generator_strategy():
    """Returns the configured generation strategy."""
    strategy = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower()
    
    if strategy == 'suno':
        return SunoSongGeneratorStrategy()
    
    # Defaults to mock for safety
    return MockSongGeneratorStrategy()