"""
Sound manager for Teeko game.
Handles loading and playing audio effects.
"""

import pygame
import os
import src.gui.config as config


class SoundManager:
    """Manages game sound effects with fallback for missing files."""
    
    def __init__(self):
        """Initialize sound manager and load all sound files."""
        pygame.mixer.init()
        self.sounds = {}
        self.enabled = config.ENABLE_SOUND
        
        # Load all sounds from config
        for name, path in config.SOUND_PATHS.items():
            self.load_sound(name, path)
    
    def load_sound(self, name, path):
        """
        Load a sound file.
        
        Args:
            name (str): Name key for the sound (e.g., 'pawn_move')
            path (str): Relative or absolute path to the sound file
        
        Returns:
            pygame.mixer.Sound or None if file not found
        """
        try:
            # Try absolute path first
            if os.path.isabs(path):
                full_path = path
            else:
                # Try relative to current working directory
                full_path = config.RESOURCE_PATH / path # os.path.join(os.getcwd(), path)
            
            if os.path.exists(full_path):
                self.sounds[name] = pygame.mixer.Sound(full_path)
                print(f"[Sound] Loaded: {name} from {full_path}")
                return self.sounds[name]
            else:
                print(f"[Sound] Warning: File not found: {full_path}")
                self.sounds[name] = None
                return None
        except Exception as e:
            print(f"[Sound] Error loading {name} from {path}: {e}")
            self.sounds[name] = None
            return None
    
    def play(self, name, volume=1.0):
        """
        Play a sound effect.
        
        Args:
            name (str): Name of the sound to play
            volume (float): Volume level (0.0 to 1.0)
        """
        if not self.enabled:
            return
        
        if name not in self.sounds:
            print(f"[Sound] Warning: Sound '{name}' not loaded")
            return
        
        sound = self.sounds[name]
        if sound is None:
            return
        
        try:
            sound.set_volume(max(0.0, min(1.0, volume)))
            sound.play()
        except Exception as e:
            print(f"[Sound] Error playing {name}: {e}")
    
    def stop_all(self):
        """Stop all currently playing sounds."""
        try:
            pygame.mixer.stop()
        except Exception as e:
            print(f"[Sound] Error stopping sounds: {e}")
    
    def set_enabled(self, enabled):
        """Enable or disable sound playback."""
        self.enabled = enabled


# Global sound manager instance
_sound_manager = None


def get_sound_manager():
    """Get or create the global sound manager."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager


def play_sound(name, volume=1.0):
    """Convenience function to play a sound."""
    manager = get_sound_manager()
    manager.play(name, volume)
