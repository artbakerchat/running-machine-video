"""
Treadmill Sensor Simulator
Simulates sensor data from a treadmill and sends it to the running-machine-video app
"""

import requests
import time
import math
from typing import Callable

class TreadmillSimulator:
    def __init__(self, backend_url: str = 'http://localhost:5000'):
        self.backend_url = backend_url
        self.speed = 0.0  # km/h
        self.distance = 0.0  # meters
        self.time_elapsed = 0.0  # seconds
        self.is_running = False

    def send_data(self) -> bool:
        """Send current state to backend"""
        try:
            response = requests.post(
                f'{self.backend_url}/api/sensor/data',
                json={'speed': self.speed, 'distance': self.distance},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

    def simulate_constant_speed(self, speed_kmh: float, duration_seconds: int, interval: float = 0.1):
        """
        Simulate running at constant speed
        
        Args:
            speed_kmh: Speed in km/h
            duration_seconds: How long to run (in seconds)
            interval: Update interval in seconds
        """
        print(f"\nSimulating constant speed: {speed_kmh} km/h for {duration_seconds}s")
        self.speed = speed_kmh
        self.is_running = True
        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            elapsed = time.time() - start_time
            # Distance = speed * time (convert km/h to m/s: km/h / 3.6 = m/s)
            self.distance = (speed_kmh / 3.6) * elapsed

            if not self.send_data():
                print("Failed to send data, stopping simulation")
                break

            print(f"Speed: {self.speed:.1f} km/h | Distance: {self.distance:.1f}m | Time: {elapsed:.1f}s")
            time.sleep(interval)

        self.speed = 0.0
        self.is_running = False
        self.send_data()
        print("Simulation stopped")

    def simulate_speed_progression(self, speed_points: list, interval: float = 0.1):
        """
        Simulate speed changes over time
        
        Args:
            speed_points: List of (duration_sec, speed_kmh) tuples
                         e.g., [(10, 8), (10, 12), (5, 15)]
                         means: 10s at 8 km/h, 10s at 12 km/h, 5s at 15 km/h
            interval: Update interval in seconds
        """
        print("\nSimulating speed progression")
        self.is_running = True
        total_time = 0

        for duration, speed_kmh in speed_points:
            print(f"\n→ Running at {speed_kmh} km/h for {duration}s")
            self.speed = speed_kmh
            start_time = time.time()

            while time.time() - start_time < duration:
                elapsed = time.time() - start_time
                # Add to total distance
                self.distance = (speed_kmh / 3.6) * (total_time + elapsed)

                if not self.send_data():
                    print("Failed to send data, stopping simulation")
                    return

                print(f"  Speed: {self.speed:.1f} km/h | Distance: {self.distance:.1f}m")
                time.sleep(interval)

            total_time += duration

        self.speed = 0.0
        self.is_running = False
        self.send_data()
        print("\nSimulation complete")

    def simulate_interval_training(self, 
                                  warm_up: tuple,
                                  intervals: list,
                                  cool_down: tuple,
                                  interval: float = 0.1):
        """
        Simulate interval training
        
        Args:
            warm_up: (duration_sec, speed_kmh)
            intervals: List of (work_duration, work_speed, rest_duration, rest_speed) tuples
            cool_down: (duration_sec, speed_kmh)
            interval: Update interval in seconds
        """
        print("\n=== INTERVAL TRAINING SIMULATION ===")
        
        # Warm up
        print(f"\nWarm-up: {warm_up[1]} km/h for {warm_up[0]}s")
        self.simulate_constant_speed(warm_up[1], warm_up[0], interval)

        # Intervals
        for i, (work_dur, work_speed, rest_dur, rest_speed) in enumerate(intervals, 1):
            print(f"\n[Interval {i}]")
            print(f"Work: {work_speed} km/h for {work_dur}s")
            self.simulate_constant_speed(work_speed, work_dur, interval)

            print(f"Rest: {rest_speed} km/h for {rest_dur}s")
            self.simulate_constant_speed(rest_speed, rest_dur, interval)

        # Cool down
        print(f"\nCool-down: {cool_down[1]} km/h for {cool_down[0]}s")
        self.simulate_constant_speed(cool_down[1], cool_down[0], interval)

        print("\n=== TRAINING COMPLETE ===")


def main():
    # Initialize simulator
    simulator = TreadmillSimulator('http://localhost:5000')

    # Test 1: Simple constant speed
    print("\n" + "="*50)
    print("TEST 1: Constant Speed (10 km/h)")
    print("="*50)
    simulator.simulate_constant_speed(10, 15, interval=0.5)

    time.sleep(2)

    # Test 2: Speed progression
    print("\n" + "="*50)
    print("TEST 2: Speed Progression")
    print("="*50)
    simulator.simulate_speed_progression(
        [(5, 8), (5, 10), (5, 12), (5, 10)],
        interval=0.5
    )

    time.sleep(2)

    # Test 3: Interval training
    print("\n" + "="*50)
    print("TEST 3: Interval Training")
    print("="*50)
    simulator.simulate_interval_training(
        warm_up=(5, 8),  # 5 seconds at 8 km/h
        intervals=[
            (3, 15, 2, 8),  # 3s hard (15 km/h), 2s easy (8 km/h)
            (3, 15, 2, 8),
            (3, 15, 2, 8),
        ],
        cool_down=(5, 6),  # 5 seconds at 6 km/h
        interval=0.5
    )


if __name__ == '__main__':
    main()
