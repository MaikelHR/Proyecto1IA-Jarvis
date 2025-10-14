"""Video capture and image processing utilities."""

from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Optional, Tuple

try:
    import cv2
    import numpy as np
    from PIL import Image
    
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠ OpenCV no disponible. Captura de video no funcionará.")


class VideoCapture:
    """Utility for capturing video from camera."""
    
    def __init__(self, camera_index: int = 0):
        """
        Initialize video capture.
        
        Args:
            camera_index: Camera device index (default: 0 for default camera)
        """
        if not CV2_AVAILABLE:
            raise ImportError(
                "OpenCV is not installed. Install it with: pip install opencv-python"
            )
        
        self.camera_index = camera_index
        self.capture: Optional[cv2.VideoCapture] = None
    
    def start(self) -> bool:
        """
        Start video capture.
        
        Returns:
            True if capture started successfully
        """
        self.capture = cv2.VideoCapture(self.camera_index)
        return self.capture.isOpened()
    
    def stop(self) -> None:
        """Stop video capture and release camera."""
        if self.capture:
            self.capture.release()
            self.capture = None
        cv2.destroyAllWindows()
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from the camera.
        
        Returns:
            Tuple of (success, frame)
        """
        if not self.capture:
            return False, None
        
        return self.capture.read()
    
    def capture_photo(self) -> Optional[np.ndarray]:
        """
        Capture a single photo from camera.
        
        Returns:
            Captured frame as numpy array
        """
        success, frame = self.read_frame()
        if success:
            return frame
        return None
    
    def capture_and_save(self, output_path: str) -> bool:
        """
        Capture a photo and save it to disk.
        
        Args:
            output_path: Path to save the image
            
        Returns:
            True if successful
        """
        frame = self.capture_photo()
        if frame is not None:
            cv2.imwrite(output_path, frame)
            return True
        return False
    
    def show_live_feed(self, window_name: str = "Camera") -> None:
        """
        Show live camera feed in a window.
        Press 'q' to quit, 's' to save snapshot.
        
        Args:
            window_name: Name of the display window
        """
        if not self.capture:
            print("Camera not started")
            return
        
        print("Presiona 'q' para salir, 's' para tomar foto")
        
        snapshot_count = 0
        while True:
            success, frame = self.read_frame()
            
            if not success:
                break
            
            # Display frame
            cv2.imshow(window_name, frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save snapshot
                output_dir = Path("temp_images")
                output_dir.mkdir(exist_ok=True)
                snapshot_path = output_dir / f"snapshot_{snapshot_count}.jpg"
                cv2.imwrite(str(snapshot_path), frame)
                print(f"Foto guardada: {snapshot_path}")
                snapshot_count += 1
        
        cv2.destroyAllWindows()
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


def frame_to_bytes(frame: np.ndarray, format: str = "JPEG") -> bytes:
    """
    Convert OpenCV frame to bytes.
    
    Args:
        frame: OpenCV frame (numpy array)
        format: Image format (JPEG, PNG, etc.)
        
    Returns:
        Image bytes
    """
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    image = Image.fromarray(frame_rgb)
    
    # Save to bytes
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    buffer.seek(0)
    
    return buffer.read()


def frame_to_base64(frame: np.ndarray, format: str = "JPEG") -> str:
    """
    Convert OpenCV frame to base64 string.
    
    Args:
        frame: OpenCV frame (numpy array)
        format: Image format
        
    Returns:
        Base64 encoded string
    """
    image_bytes = frame_to_bytes(frame, format)
    return base64.b64encode(image_bytes).decode('utf-8')


def base64_to_bytes(base64_string: str) -> bytes:
    """
    Convert base64 string to bytes.
    
    Args:
        base64_string: Base64 encoded string
        
    Returns:
        Decoded bytes
    """
    return base64.b64decode(base64_string)


def bytes_to_frame(image_bytes: bytes) -> np.ndarray:
    """
    Convert image bytes to OpenCV frame.
    
    Args:
        image_bytes: Image bytes
        
    Returns:
        OpenCV frame (numpy array)
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Decode image
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    return frame


def resize_frame(
    frame: np.ndarray,
    width: Optional[int] = None,
    height: Optional[int] = None,
    max_dimension: Optional[int] = None
) -> np.ndarray:
    """
    Resize frame maintaining aspect ratio.
    
    Args:
        frame: Input frame
        width: Target width
        height: Target height
        max_dimension: Maximum dimension (width or height)
        
    Returns:
        Resized frame
    """
    h, w = frame.shape[:2]
    
    if max_dimension:
        if w > h:
            width = max_dimension
            height = int(h * (max_dimension / w))
        else:
            height = max_dimension
            width = int(w * (max_dimension / h))
    
    elif width and not height:
        height = int(h * (width / w))
    
    elif height and not width:
        width = int(w * (height / h))
    
    if width and height:
        return cv2.resize(frame, (width, height))
    
    return frame


def draw_face_rectangle(
    frame: np.ndarray,
    face_rectangle: dict,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    Draw rectangle around detected face.
    
    Args:
        frame: Input frame
        face_rectangle: Dictionary with left, top, width, height
        color: Rectangle color (BGR)
        thickness: Line thickness
        
    Returns:
        Frame with rectangle drawn
    """
    left = face_rectangle["left"]
    top = face_rectangle["top"]
    width = face_rectangle["width"]
    height = face_rectangle["height"]
    
    cv2.rectangle(
        frame,
        (left, top),
        (left + width, top + height),
        color,
        thickness
    )
    
    return frame


def add_text_to_frame(
    frame: np.ndarray,
    text: str,
    position: Tuple[int, int],
    color: Tuple[int, int, int] = (0, 255, 0),
    font_scale: float = 0.7,
    thickness: int = 2
) -> np.ndarray:
    """
    Add text overlay to frame.
    
    Args:
        frame: Input frame
        text: Text to add
        position: Text position (x, y)
        color: Text color (BGR)
        font_scale: Font scale
        thickness: Text thickness
        
    Returns:
        Frame with text
    """
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness
    )
    
    return frame


def get_available_cameras() -> list:
    """
    Get list of available camera indices.
    
    Returns:
        List of available camera indices
    """
    if not CV2_AVAILABLE:
        return []
    
    available = []
    for i in range(10):  # Check first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    
    return available


def print_available_cameras() -> None:
    """Print available cameras."""
    cameras = get_available_cameras()
    
    print("\n📹 Cámaras disponibles:")
    print("=" * 60)
    
    if not cameras:
        print("  No se encontraron cámaras")
    else:
        for idx in cameras:
            print(f"  [{idx}] Cámara {idx}")
    
    print("=" * 60)
