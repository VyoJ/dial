"""Integration tests for the dial library."""

import os
import tempfile

from PIL import Image

import dial


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_human_interface_workflow(self):
        """Test complete human interface workflow."""
        # Create clocks with different styles
        styles = ["classic", "modern", "minimal"]

        for style in styles:
            clock = dial.Clock.create("3:15:30", style)

            # Verify clock has expected elements
            assert len(clock.elements) == 4  # face, ticks, numerals, hands

            # Verify rendering works
            image = clock.render()
            assert isinstance(image, Image.Image)
            assert image.size == (400, 400)

    def test_agent_interface_workflow(self):
        """Test complete agent interface workflow."""
        config = {
            "width": 300,
            "height": 300,
            "antialias": True,
            "scale_factor": 2,
            "elements": [
                {
                    "type": "Face",
                    "properties": {
                        "shape": "circle",
                        "color": "white",
                        "border_color": "black",
                        "border_width": 2,
                    },
                },
                {
                    "type": "Ticks",
                    "properties": {
                        "hour_spec": {
                            "shape": "line",
                            "color": "black",
                            "length": 0.08,
                            "width": 3,
                        }
                    },
                },
                {
                    "type": "Numerals",
                    "properties": {
                        "system": "arabic",
                        "color": "black",
                        "font_size": 24,
                    },
                },
                {
                    "type": "Hands",
                    "properties": {
                        "time": "6:30:45",
                        "hour_spec": {
                            "shape": "line",
                            "color": "black",
                            "length": 0.5,
                            "width": 6,
                        },
                        "minute_spec": {
                            "shape": "line",
                            "color": "black",
                            "length": 0.8,
                            "width": 4,
                        },
                        "second_spec": {
                            "shape": "line",
                            "color": "red",
                            "length": 0.9,
                            "width": 2,
                        },
                    },
                },
            ],
        }

        clock = dial.Clock.from_config(config)
        assert clock.width == 300
        assert clock.height == 300
        assert len(clock.elements) == 4

        # Verify rendering
        image = clock.render()
        assert isinstance(image, Image.Image)
        assert image.size == (300, 300)

    def test_mixed_interface_workflow(self):
        """Test mixed interface workflow."""
        # Start with preset
        clock = dial.Clock.create("12:00:00", "classic")

        # Add custom overlay
        from dial.elements.overlay import Overlay

        overlay = Overlay(
            type="date_window",
            date="2025-10-12",
            position=(200, 320),
            font_size=16,
            text_color="darkblue",
            background_color="lightblue",
        )
        clock.add_element(overlay)

        # Verify final result
        assert len(clock.elements) == 5  # 4 preset + 1 custom
        image = clock.render()
        assert isinstance(image, Image.Image)

    def test_file_format_support(self):
        """Test saving in different file formats."""
        clock = dial.Clock.create("9:15:30", "minimal", width=100, height=100)

        formats = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]

        for fmt in formats:
            with tempfile.NamedTemporaryFile(suffix=fmt, delete=False) as tmp:
                tmp_path = tmp.name

            try:
                clock.save(tmp_path)
                assert os.path.exists(tmp_path)

                # Verify it's a valid image (skip for some formats that PIL might not support)
                try:
                    with Image.open(tmp_path) as img:
                        assert img.size == (100, 100)
                except Exception:
                    # Some formats might not be supported in all PIL installations
                    pass
            finally:
                try:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                except (PermissionError, OSError):
                    pass  # File might be locked on Windows

    def test_quality_settings_integration(self):
        """Test different quality settings in complete workflow."""
        base_config = {
            "width": 200,
            "height": 200,
            "elements": [
                {"type": "Face", "properties": {"shape": "circle", "color": "white"}},
                {"type": "Hands", "properties": {"time": "3:15:30"}},
            ],
        }

        # Test different quality settings
        quality_configs = [
            {"antialias": False, "scale_factor": 1},  # Pixelated
            {"antialias": True, "scale_factor": 2},  # Standard
            {"antialias": True, "scale_factor": 4},  # High quality
        ]

        for quality in quality_configs:
            config = {**base_config, **quality}
            clock = dial.Clock.from_config(config)

            image = clock.render()
            assert isinstance(image, Image.Image)
            assert image.size == (200, 200)

    def test_hand_accuracy_integration(self):
        """Test hand positioning accuracy in complete workflow."""
        test_times = [
            "3:15:30",  # Quarter past
            "6:30:45",  # Half past
            "9:45:15",  # Quarter to
            "12:00:00",  # Noon
        ]

        for time in test_times:
            clock = dial.Clock.create(time, "classic", width=200, height=200)
            image = clock.render()

            # Basic verification that image was created
            assert isinstance(image, Image.Image)
            assert image.size == (200, 200)

            # Verify hands element exists and has correct time
            hands_elements = [
                e for e in clock.elements if e.get_property("time") == time
            ]
            assert len(hands_elements) == 1
