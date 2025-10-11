"""Tests for element classes."""

from dial.elements import Face, Hands, Numerals, Overlay, Ticks


class TestFace:
    """Test Face element."""

    def test_face_initialization(self):
        """Test Face initialization."""
        face = Face(shape="circle", color="white")
        assert face.get_property("shape") == "circle"
        assert face.get_property("color") == "white"
        assert face.z_order == 0

    def test_face_with_border(self):
        """Test Face with border."""
        face = Face(shape="circle", color="white", border_color="black", border_width=3)
        assert face.get_property("border_color") == "black"
        assert face.get_property("border_width") == 3


class TestTicks:
    """Test Ticks element."""

    def test_ticks_initialization(self):
        """Test Ticks initialization."""
        ticks = Ticks(
            hour_spec={"shape": "line", "color": "black", "length": 0.08, "width": 3},
            minute_spec={"shape": "line", "color": "black", "length": 0.04, "width": 1},
        )
        assert ticks.get_property("hour_spec")["color"] == "black"
        assert ticks.get_property("minute_spec")["length"] == 0.04
        assert ticks.z_order == 1

    def test_ticks_hour_only(self):
        """Test Ticks with hour marks only."""
        ticks = Ticks(
            hour_spec={"shape": "line", "color": "black", "length": 0.08, "width": 3}
        )
        assert ticks.get_property("hour_spec") is not None
        assert ticks.get_property("minute_spec") is None


class TestNumerals:
    """Test Numerals element."""

    def test_numerals_arabic(self):
        """Test Numerals with Arabic numerals."""
        numerals = Numerals(system="arabic", color="black", font_size=28)
        assert numerals.get_property("system") == "arabic"
        assert numerals.get_property("color") == "black"
        assert numerals.get_property("font_size") == 28
        assert numerals.z_order == 2

    def test_numerals_roman(self):
        """Test Numerals with Roman numerals."""
        numerals = Numerals(system="roman", color="white", font_size=32)
        assert numerals.get_property("system") == "roman"
        assert numerals.get_property("color") == "white"

    def test_numerals_with_visible_subset(self):
        """Test Numerals with only certain numbers visible."""
        numerals = Numerals(
            system="arabic", color="black", font_size=24, visible=[12, 3, 6, 9]
        )
        assert numerals.get_property("visible") == [12, 3, 6, 9]


class TestHands:
    """Test Hands element."""

    def test_hands_initialization(self):
        """Test Hands initialization."""
        hands = Hands(
            time="3:15:30",
            hour_spec={"shape": "line", "color": "black", "length": 0.5, "width": 6},
            minute_spec={"shape": "line", "color": "black", "length": 0.8, "width": 4},
            second_spec={"shape": "line", "color": "red", "length": 0.9, "width": 2},
        )
        assert hands.get_property("time") == "3:15:30"
        assert hands.get_property("hour_spec")["color"] == "black"
        assert hands.get_property("minute_spec")["length"] == 0.8
        assert hands.get_property("second_spec")["color"] == "red"
        assert hands.z_order == 4

    def test_hands_without_seconds(self):
        """Test Hands without second hand."""
        hands = Hands(
            time="6:30:00",
            hour_spec={"shape": "line", "color": "black", "length": 0.5, "width": 6},
            minute_spec={"shape": "line", "color": "black", "length": 0.8, "width": 4},
        )
        assert hands.get_property("second_spec") is None

    def test_hands_with_pivot(self):
        """Test Hands with pivot point."""
        hands = Hands(
            time="9:45:15",
            hour_spec={"shape": "line", "color": "black", "length": 0.5, "width": 6},
            minute_spec={"shape": "line", "color": "black", "length": 0.8, "width": 4},
            pivot_spec={"shape": "circle", "color": "black", "radius": 5},
        )
        assert hands.get_property("pivot_spec")["radius"] == 5


class TestOverlay:
    """Test Overlay element."""

    def test_overlay_date_window(self):
        """Test Overlay with date window."""
        overlay = Overlay(
            type="date_window",
            date="2025-01-08",
            position=(200, 300),
            font_size=18,
            text_color="black",
            background_color="white",
        )
        assert overlay.get_property("type") == "date_window"
        assert overlay.get_property("date") == "2025-01-08"
        assert overlay.get_property("position") == (200, 300)
        assert overlay.z_order == 3
