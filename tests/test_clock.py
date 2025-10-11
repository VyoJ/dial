"""Tests for the Clock class."""

import os
import tempfile

from PIL import Image

import dial


class TestClockInitialization:
    """Test Clock class initialization."""

    def test_default_initialization(self):
        """Test Clock initialization with default parameters."""
        clock = dial.Clock()
        assert clock.width == 400
        assert clock.height == 400
        assert clock.antialias is True
        assert clock.scale_factor == 2
        assert len(clock.elements) == 0

    def test_custom_initialization(self):
        """Test Clock initialization with custom parameters."""
        clock = dial.Clock(width=600, height=600, antialias=False, scale_factor=1)
        assert clock.width == 600
        assert clock.height == 600
        assert clock.antialias is False
        assert clock.scale_factor == 1

    def test_invalid_dimensions(self):
        """Test Clock initialization with invalid dimensions."""
        try:
            dial.Clock(width=-100)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Width must be a positive integer" in str(e)

        try:
            dial.Clock(height=0)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Height must be a positive integer" in str(e)

    def test_invalid_scale_factor(self):
        """Test Clock initialization with invalid scale factor."""
        try:
            dial.Clock(scale_factor=0)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Scale factor must be a positive integer" in str(e)


class TestClockCreate:
    """Test Clock.create() method for human-friendly interface."""

    def test_create_classic_style(self):
        """Test creating a clock with classic style."""
        clock = dial.Clock.create("3:15:30", "classic")
        assert clock.width == 400
        assert clock.height == 400
        assert len(clock.elements) == 4  # face, ticks, numerals, hands

    def test_create_modern_style(self):
        """Test creating a clock with modern style."""
        clock = dial.Clock.create("6:30:45", "modern")
        assert len(clock.elements) == 4

    def test_create_minimal_style(self):
        """Test creating a clock with minimal style."""
        clock = dial.Clock.create("9:45:15", "minimal")
        assert len(clock.elements) == 4

    def test_create_with_custom_dimensions(self):
        """Test creating a clock with custom dimensions."""
        clock = dial.Clock.create("12:00:00", "classic", width=600, height=600)
        assert clock.width == 600
        assert clock.height == 600

    def test_create_invalid_style(self):
        """Test creating a clock with invalid style."""
        try:
            dial.Clock.create("3:15:30", "invalid")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Style 'invalid' not recognized" in str(e)


class TestClockFromConfig:
    """Test Clock.from_config() method for agent-friendly interface."""

    def test_from_config_basic(self):
        """Test creating a clock from basic configuration."""
        config = {
            "width": 400,
            "height": 400,
            "elements": [
                {"type": "Face", "properties": {"shape": "circle", "color": "white"}}
            ],
        }
        clock = dial.Clock.from_config(config)
        assert clock.width == 400
        assert clock.height == 400
        assert len(clock.elements) == 1

    def test_from_config_complex(self):
        """Test creating a clock from complex configuration."""
        config = {
            "width": 500,
            "height": 500,
            "antialias": True,
            "scale_factor": 3,
            "elements": [
                {"type": "Face", "properties": {"shape": "circle", "color": "white"}},
                {"type": "Hands", "properties": {"time": "3:15:30"}},
            ],
        }
        clock = dial.Clock.from_config(config)
        assert clock.width == 500
        assert clock.height == 500
        assert clock.scale_factor == 3
        assert len(clock.elements) == 2


class TestClockRendering:
    """Test Clock rendering functionality."""

    def test_render_empty_clock(self):
        """Test rendering an empty clock."""
        clock = dial.Clock(width=200, height=200)
        image = clock.render()
        assert isinstance(image, Image.Image)
        assert image.size == (200, 200)

    def test_render_with_elements(self):
        """Test rendering a clock with elements."""
        clock = dial.Clock.create("12:00:00", "classic", width=200, height=200)
        image = clock.render()
        assert isinstance(image, Image.Image)
        assert image.size == (200, 200)

    def test_save_png(self):
        """Test saving clock as PNG."""
        clock = dial.Clock.create("3:15:30", "classic", width=100, height=100)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            clock.save(tmp_path)
            assert os.path.exists(tmp_path)

            # Verify it's a valid image
            with Image.open(tmp_path) as img:
                assert img.size == (100, 100)
        finally:
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except (PermissionError, OSError):
                pass  # File might be locked on Windows

    def test_save_jpg(self):
        """Test saving clock as JPEG."""
        clock = dial.Clock.create("6:30:00", "classic", width=100, height=100)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            clock.save(tmp_path)
            assert os.path.exists(tmp_path)

            # Verify it's a valid image
            with Image.open(tmp_path) as img:
                assert img.size == (100, 100)
        finally:
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except (PermissionError, OSError):
                pass  # File might be locked on Windows
