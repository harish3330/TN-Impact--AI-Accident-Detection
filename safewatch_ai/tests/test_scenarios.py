import pytest
import numpy as np
import cv2
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.video_capture import VideoCapture
from src.detector import SafetyDetector
from src.rule_engine import RuleEngine
from src.alert_system import AlertManager
from src.utils.geometry import GeometryUtils
from src.utils.tracking import ObjectTracker


class TestGeometryUtils:
    """Test geometric utility functions."""
    
    def test_point_in_polygon(self):
        """Test point in polygon detection."""
        polygon = [(0, 0), (100, 0), (100, 100), (0, 100)]
        
        # Point inside
        assert GeometryUtils.point_in_polygon((50, 50), polygon) == True
        
        # Point outside
        assert GeometryUtils.point_in_polygon((150, 150), polygon) == False
    
    def test_get_centroid(self):
        """Test centroid calculation."""
        bbox = (10, 20, 110, 120)
        cx, cy = GeometryUtils.get_centroid(bbox)
        assert cx == 60
        assert cy == 70
    
    def test_distance_between_points(self):
        """Test distance calculation."""
        distance = GeometryUtils.distance_between_points((0, 0), (3, 4))
        assert abs(distance - 5.0) < 0.01
    
    def test_bbox_aspect_ratio(self):
        """Test aspect ratio calculation."""
        # Standing person (tall)
        bbox = (10, 10, 30, 130)  # 20x120
        aspect_ratio = GeometryUtils.get_bbox_aspect_ratio(bbox)
        assert abs(aspect_ratio - 6.0) < 0.01


class TestDetector:
    """Test YOLO detector."""
    
    def test_detector_initialization(self):
        """Test detector can be initialized."""
        detector = SafetyDetector(model_name="yolov8n.pt")
        assert detector.model is not None
    
    def test_detect_on_dummy_frame(self):
        """Test detection on dummy frame."""
        detector = SafetyDetector(model_name="yolov8n.pt")
        
        # Create dummy frame
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        frame[100:200, 100:200] = 255  # White square
        
        # Should return valid structure even with no real detections
        result = detector.detect(frame)
        assert "persons" in result
        assert "vehicles" in result
        assert "ppe" in result


class TestRuleEngine:
    """Test rule engine."""
    
    def test_rule_engine_initialization(self):
        """Test rule engine can be initialized."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            config = {
                "cameras": {
                    "camera_1": {
                        "restricted_zones": [],
                        "fall_detection": True
                    }
                }
            }
            json.dump(config, f)
            config_path = f.name
        
        rule_engine = RuleEngine(config_path)
        assert rule_engine.config is not None
        
        # Cleanup
        Path(config_path).unlink()
    
    def test_fall_detection(self):
        """Test fall detection logic."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            config = {
                "cameras": {
                    "camera_1": {
                        "fall_detection": True,
                        "restricted_zones": []
                    }
                }
            }
            json.dump(config, f)
            config_path = f.name
        
        rule_engine = RuleEngine(config_path)
        
        # Test lying down person (high aspect ratio)
        detections = {
            "persons": [
                [100, 100, 300, 120, 0.95, 1]  # Wide bbox (lying down)
            ],
            "vehicles": []
        }
        
        incidents = rule_engine.check_incidents(detections, "camera_1", 1)
        # Should not trigger immediately, needs 3+ seconds
        assert len(incidents) == 0
        
        # Cleanup
        Path(config_path).unlink()


class TestAlertManager:
    """Test alert system."""
    
    def test_alert_manager_initialization(self):
        """Test alert manager initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            alert_manager = AlertManager(tmpdir)
            assert alert_manager.incident_dir.exists()
    
    def test_save_snapshot(self):
        """Test snapshot saving."""
        with tempfile.TemporaryDirectory() as tmpdir:
            alert_manager = AlertManager(tmpdir)
            
            # Create dummy frame
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame[100:200, 100:200] = [0, 255, 0]
            
            # Create dummy incident
            incident = {
                "type": "TEST_INCIDENT",
                "camera_id": "camera_1",
                "bbox": (100, 100, 200, 200),
                "timestamp": None,
                "details": "Test"
            }
            
            snapshot_path = alert_manager._save_snapshot(frame, incident)
            
            assert snapshot_path is not None
            assert Path(snapshot_path).exists()


class TestObjectTracker:
    """Test object tracking."""
    
    def test_tracker_initialization(self):
        """Test tracker initialization."""
        tracker = ObjectTracker()
        assert tracker.next_track_id == 1
    
    def test_track_update(self):
        """Test track update."""
        tracker = ObjectTracker()
        
        # Detection 1
        detections = [
            {"bbox": (100, 100, 200, 200), "class_name": "person", "confidence": 0.9}
        ]
        
        tracks = tracker.update(detections)
        assert len(tracks) == 1


def test_demo_scenario_fall():
    """Test fall detection scenario."""
    print("\n=== Fall Detection Test ===")
    
    # Create a sequence of bounding boxes that represent a falling person
    fall_sequence = [
        (100, 50, 150, 250),   # Frame 1: Standing (tall, narrow)
        (100, 60, 180, 280),   # Frame 2: Falling (getting wider)
        (80, 120, 280, 180),   # Frame 3: Lying down (wide, short)
        (80, 120, 280, 180),   # Frame 4: Lying down
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        import json
        config = {
            "cameras": {
                "camera_1": {
                    "fall_detection": True,
                    "restricted_zones": []
                }
            }
        }
        json.dump(config, f)
        config_path = f.name
    
    rule_engine = RuleEngine(config_path)
    
    for i, bbox in enumerate(fall_sequence):
        detections = {
            "persons": [list(bbox) + [0.95, 1]],
            "vehicles": []
        }
        incidents = rule_engine.check_incidents(detections, "camera_1", i + 1)
        print(f"Frame {i+1}: Aspect Ratio = {GeometryUtils.get_bbox_aspect_ratio(bbox):.2f}")
    
    Path(config_path).unlink()
    print("✓ Fall detection test passed\n")


def test_demo_scenario_proximity():
    """Test proximity detection scenario."""
    print("=== Proximity Detection Test ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        import json
        config = {
            "cameras": {
                "camera_1": {
                    "proximity_threshold_px": 50,
                    "restricted_zones": [],
                    "fall_detection": False
                }
            }
        }
        json.dump(config, f)
        config_path = f.name
    
    rule_engine = RuleEngine(config_path)
    
    # Person and vehicle getting closer
    for distance in [200, 100, 50, 40, 30]:
        detections = {
            "persons": [[100, 100, 150, 250, 0.95, 1]],
            "vehicles": [[distance, 100, distance + 100, 200, 0.95, 2]]
        }
        incidents = rule_engine.check_incidents(detections, "camera_1", 1)
        print(f"Distance: {distance}px -> Incidents: {len(incidents)}")
    
    Path(config_path).unlink()
    print("✓ Proximity detection test passed\n")


if __name__ == "__main__":
    # Run demo scenarios
    test_demo_scenario_fall()
    test_demo_scenario_proximity()
    
    # Run pytest
    pytest.main([__file__, "-v"])
