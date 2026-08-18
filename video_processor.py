"""
Advanced video processing for Running Machine
Optional: Process videos to enhance the illusion of speed
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple

class VideoProcessor:
    """
    Optional video processing to enhance the running experience.
    This can add effects like motion blur or brightness adjustments.
    """

    @staticmethod
    def apply_motion_blur(frame: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """
        Apply subtle motion blur to simulate speed
        
        Args:
            frame: Input frame
            intensity: Blur intensity (0.0 to 1.0)
        
        Returns:
            Blurred frame
        """
        if intensity <= 0:
            return frame

        # Create horizontal motion blur kernel
        size = int(intensity * 30) + 1
        if size % 2 == 0:
            size += 1

        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (size, 1)
        )
        kernel = kernel / kernel.sum()

        blurred = cv2.filter2D(frame, -1, kernel)
        return cv2.addWeighted(frame, 0.7, blurred, 0.3, 0)

    @staticmethod
    def adjust_brightness(frame: np.ndarray, speed: float, base_speed: float = 10) -> np.ndarray:
        """
        Adjust brightness based on speed perception
        
        Args:
            frame: Input frame
            speed: Current speed (km/h)
            base_speed: Base speed for normal brightness
        
        Returns:
            Brightness-adjusted frame
        """
        # Slight brightness boost when running faster
        speed_ratio = speed / base_speed
        brightness_factor = 0.95 + (speed_ratio * 0.1)  # Range: 0.95 to 1.25
        brightness_factor = np.clip(brightness_factor, 0.8, 1.3)

        adjusted = cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)
        return np.uint8(np.clip(adjusted, 0, 255))

    @staticmethod
    def create_speed_indicator(frame: np.ndarray, speed: float, playback_rate: float) -> np.ndarray:
        """
        Add visual speed indicator overlay on frame
        
        Args:
            frame: Input frame
            speed: Current speed (km/h)
            playback_rate: Video playback rate
        
        Returns:
            Frame with speed indicator
        """
        h, w = frame.shape[:2]

        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (w - 300, 20), (w - 20, 120), (0, 0, 0), -1)

        # Blend overlay
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        # Add text
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)

        cv2.putText(frame, f"Speed: {speed:.1f} km/h", (w - 280, 50),
                   font, 0.7, color, 2)
        cv2.putText(frame, f"Playback: {playback_rate:.2f}x", (w - 280, 85),
                   font, 0.7, color, 2)

        return frame

    @staticmethod
    def process_frame(frame: np.ndarray,
                     speed: float,
                     base_speed: float = 10,
                     enable_blur: bool = True,
                     enable_brightness: bool = True,
                     show_indicator: bool = False) -> np.ndarray:
        """
        Apply all video effects to a frame
        
        Args:
            frame: Input frame
            speed: Current speed (km/h)
            base_speed: Base speed for normalization
            enable_blur: Apply motion blur
            enable_brightness: Adjust brightness
            show_indicator: Show speed indicator overlay
        
        Returns:
            Processed frame
        """
        processed = frame.copy()

        if enable_blur:
            blur_intensity = min((speed / base_speed) * 0.3, 1.0)
            processed = VideoProcessor.apply_motion_blur(processed, blur_intensity)

        if enable_brightness:
            processed = VideoProcessor.adjust_brightness(processed, speed, base_speed)

        if show_indicator:
            playback_rate = (speed / base_speed)
            playback_rate = np.clip(playback_rate, 0.5, 2.0)
            processed = VideoProcessor.create_speed_indicator(
                processed, speed, playback_rate
            )

        return processed


# Example usage and testing
if __name__ == '__main__':
    print("Video Processing Module Loaded")
    print("\nFeatures:")
    print("- Motion blur based on speed")
    print("- Dynamic brightness adjustment")
    print("- Speed indicator overlay")
    print("\nTo use in your application:")
    print("1. Capture video frames")
    print("2. Process with VideoProcessor.process_frame()")
    print("3. Send to video output")
