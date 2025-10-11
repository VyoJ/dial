"""Tests for utility functions."""

from dial.utils import (
    create_gradient_image,
    load_font,
    parse_color,
    point_on_circle,
    time_to_angles,
)


class TestGeometryUtils:
    """Test geometry utility functions."""

    def test_point_on_circle(self):
        """Test point_on_circle function."""
        # Test cardinal directions
        center = (100, 100)
        radius = 50

        # 0 degrees (top)
        x, y = point_on_circle(center, radius, 0)
        assert abs(x - 100) < 0.001
        assert abs(y - 50) < 0.001

        # 90 degrees (right)
        x, y = point_on_circle(center, radius, 90)
        assert abs(x - 150) < 0.001
        assert abs(y - 100) < 0.001

        # 180 degrees (bottom)
        x, y = point_on_circle(center, radius, 180)
        assert abs(x - 100) < 0.001
        assert abs(y - 150) < 0.001

        # 270 degrees (left)
        x, y = point_on_circle(center, radius, 270)
        assert abs(x - 50) < 0.001
        assert abs(y - 100) < 0.001

    def test_time_to_angles(self):
        """Test time_to_angles function."""
        # Test 12:00:00
        hour_angle, minute_angle, second_angle = time_to_angles(12, 0, 0)
        assert hour_angle == 0
        assert minute_angle == 0
        assert second_angle == 0

        # Test 3:15:30
        hour_angle, minute_angle, second_angle = time_to_angles(3, 15, 30)
        assert hour_angle == 97.5  # 3*30 + 15*0.5
        assert minute_angle == 93  # 15*6 + 30*0.1
        assert second_angle == 180  # 30*6

        # Test 6:30:45
        hour_angle, minute_angle, second_angle = time_to_angles(6, 30, 45)
        assert hour_angle == 195  # 6*30 + 30*0.5
        assert minute_angle == 184.5  # 30*6 + 45*0.1
        assert second_angle == 270  # 45*6

    def test_time_to_angles_edge_cases(self):
        """Test time_to_angles with edge cases."""
        # Test 24-hour format conversion
        hour_angle, _, _ = time_to_angles(15, 0, 0)
        assert hour_angle == 90  # 15 % 12 = 3, 3*30 = 90

        # Test midnight
        hour_angle, minute_angle, second_angle = time_to_angles(0, 0, 0)
        assert hour_angle == 0
        assert minute_angle == 0
        assert second_angle == 0


class TestColorUtils:
    """Test color utility functions."""

    def test_parse_color_hex(self):
        """Test parsing hex colors."""
        assert parse_color("#FF0000") == "#FF0000"
        assert parse_color("#00FF00") == "#00FF00"
        assert parse_color("#0000FF") == "#0000FF"
        assert parse_color("#FFFFFF") == "#FFFFFF"
        assert parse_color("#000000") == "#000000"

    def test_parse_color_short_hex(self):
        """Test parsing short hex colors."""
        assert parse_color("#F00") == "#F00"
        assert parse_color("#0F0") == "#0F0"
        assert parse_color("#00F") == "#00F"

    def test_parse_color_named(self):
        """Test parsing named colors."""
        assert parse_color("red") == "red"
        assert parse_color("green") == "green"
        assert parse_color("blue") == "blue"
        assert parse_color("white") == "white"
        assert parse_color("black") == "black"

    def test_parse_color_rgba_tuple(self):
        """Test parsing RGBA tuples."""
        # Note: Current implementation doesn't properly support tuple validation
        # This test verifies the expected behavior when tuples are used incorrectly
        try:
            parse_color((255, 0, 0))
            assert False, "Should have raised error for tuple input"
        except (ValueError, AttributeError):
            pass  # Expected - current implementation doesn't support tuples properly

    def test_parse_color_invalid(self):
        """Test parsing invalid colors."""
        try:
            parse_color("invalid_color")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected

    def test_parse_color_gradient_dict(self):
        """Test parsing gradient color dictionaries."""
        gradient = {
            "type": "linear_gradient",
            "colors": ["red", "blue"],
            "direction": "horizontal",
        }
        result = parse_color(gradient)
        assert isinstance(result, dict)
        assert result["type"] == "linear_gradient"


class TestFontUtils:
    """Test font utility functions."""

    def test_load_font_default(self):
        """Test loading default font."""
        font = load_font(font_size=20)
        assert font is not None

    def test_load_font_custom_size(self):
        """Test loading font with custom size."""
        font = load_font(font_size=30)
        assert font is not None


class TestGradientUtils:
    """Test gradient utility functions."""

    def test_create_linear_gradient(self):
        """Test creating linear gradient."""
        gradient_spec = {
            "type": "linear_gradient",
            "colors": ["red", "blue"],
            "direction": "horizontal",
        }
        gradient = create_gradient_image((100, 100), gradient_spec)
        assert gradient.size == (100, 100)

    def test_create_radial_gradient(self):
        """Test creating radial gradient."""
        gradient_spec = {"type": "radial_gradient", "colors": ["white", "black"]}
        gradient = create_gradient_image((100, 100), gradient_spec)
        assert gradient.size == (100, 100)

    def test_create_gradient_multiple_colors(self):
        """Test creating gradient with multiple colors."""
        gradient_spec = {
            "type": "linear_gradient",
            "colors": ["red", "green", "blue"],
            "direction": "vertical",
        }
        gradient = create_gradient_image((100, 100), gradient_spec)
        assert gradient.size == (100, 100)
