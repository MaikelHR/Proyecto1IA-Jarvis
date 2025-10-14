"""Audio capture and processing utilities."""

from __future__ import annotations

import io
import wave
from typing import Optional

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("⚠ PyAudio no disponible. Captura de audio no funcionará.")


class AudioRecorder:
    """Utility for recording audio from microphone."""
    
    # Audio configuration
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
    CHANNELS = 1
    RATE = 16000
    
    def __init__(self):
        """Initialize audio recorder."""
        if not PYAUDIO_AVAILABLE:
            raise ImportError(
                "PyAudio is not installed. Install it with: pip install pyaudio"
            )
        
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.frames = []
    
    def start_recording(self) -> None:
        """Start recording audio from microphone."""
        self.frames = []
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        print("🎤 Grabación iniciada...")
    
    def stop_recording(self) -> bytes:
        """
        Stop recording and return audio data.
        
        Returns:
            Raw audio bytes
        """
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        print("🎤 Grabación detenida")
        
        # Convert frames to bytes
        audio_data = b''.join(self.frames)
        return audio_data
    
    def record_chunk(self) -> None:
        """Record a single chunk of audio."""
        if self.stream:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            self.frames.append(data)
    
    def record_duration(self, duration_seconds: float) -> bytes:
        """
        Record audio for a specific duration.
        
        Args:
            duration_seconds: Duration to record in seconds
            
        Returns:
            Raw audio bytes
        """
        self.start_recording()
        
        num_chunks = int(self.RATE / self.CHUNK * duration_seconds)
        
        for _ in range(num_chunks):
            self.record_chunk()
        
        return self.stop_recording()
    
    def save_to_wav(self, audio_data: bytes, output_path: str) -> None:
        """
        Save audio data to WAV file.
        
        Args:
            audio_data: Raw audio bytes
            output_path: Path to save WAV file
        """
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
        
        print(f"💾 Audio guardado en: {output_path}")
    
    def get_wav_bytes(self, audio_data: bytes) -> bytes:
        """
        Convert raw audio to WAV format bytes.
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            WAV formatted bytes
        """
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
        
        return wav_buffer.getvalue()
    
    def cleanup(self) -> None:
        """Cleanup audio resources."""
        if self.stream:
            self.stream.close()
        self.audio.terminate()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


def get_available_devices() -> list:
    """
    Get list of available audio input devices.
    
    Returns:
        List of device information dictionaries
    """
    if not PYAUDIO_AVAILABLE:
        return []
    
    audio = pyaudio.PyAudio()
    devices = []
    
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            devices.append({
                'index': i,
                'name': device_info['name'],
                'channels': device_info['maxInputChannels'],
                'sample_rate': int(device_info['defaultSampleRate'])
            })
    
    audio.terminate()
    return devices


def print_available_devices() -> None:
    """Print available audio input devices."""
    devices = get_available_devices()
    
    print("\n🎤 Dispositivos de audio disponibles:")
    print("=" * 60)
    
    if not devices:
        print("  No se encontraron dispositivos de entrada")
    else:
        for device in devices:
            print(f"  [{device['index']}] {device['name']}")
            print(f"      Canales: {device['channels']}, "
                  f"Sample Rate: {device['sample_rate']} Hz")
    
    print("=" * 60)
