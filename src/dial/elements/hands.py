"""Hands element for hour, minute, and second hands."""

import math
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw

from dial.element import Element
from dial.utils import (
    parse_color,
    point_on_circle,
    time_to_angles,
    validate_time_format,
)


class Hands(Element):
    """Clock hands element for displaying time."""

    @property
    def z_order(self) -> int:
        """Hands are drawn on top of all other elements."""
        return 4

    def _validate_properties(self) -> None:
        """Validate Hands element properties."""
        # Validate time format
        time_str = self.get_property("time")
        if time_str is not None:
            validate_time_format(time_str)

        # Validate mode
        mode = self.get_property("mode", "12h")
        if mode not in ["12h", "24h"]:
            raise ValueError("mode must be '12h' or '24h'")

        # Validate hand specifications
        hour_spec = self.get_property("hour_spec")
        if hour_spec:
            self._validate_hand_spec(hour_spec, "hour_spec")

        minute_spec = self.get_property("minute_spec")
        if minute_spec:
            self._validate_hand_spec(minute_spec, "minute_spec")

        second_spec = self.get_property("second_spec")
        if second_spec:
            self._validate_hand_spec(second_spec, "second_spec")

        # Validate pivot specification
        pivot_spec = self.get_property("pivot_spec")
        if pivot_spec:
            self._validate_pivot_spec(pivot_spec)

        # Validate hands array (new flexible format)
        hands = self.get_property("hands")
        if hands is not None:
            if not isinstance(hands, list):
                raise ValueError("hands must be a list")
            for hand in hands:
                if not isinstance(hand, dict):
                    raise ValueError("each hand must be a dictionary")
                self._validate_hand_spec(hand, "hand")

    def _validate_hand_spec(self, spec: Dict[str, Any], spec_name: str) -> None:
        """Validate a hand specification dictionary."""
        # Validate shape
        shape = spec.get("shape", "line")
        if shape not in ["line", "triangle", "custom_polygon"]:
            raise ValueError(
                f"{spec_name} shape must be 'line', 'triangle', or 'custom_polygon'"
            )

        # Validate custom_polygon if shape is custom_polygon
        if shape == "custom_polygon":
            custom_polygon = spec.get("custom_polygon")
            if not custom_polygon:
                raise ValueError(
                    f"{spec_name} requires 'custom_polygon' when shape is 'custom_polygon'"
                )
            if not isinstance(custom_polygon, list):
                raise ValueError(
                    f"{spec_name} custom_polygon must be a list of (x, y) tuples"
                )
            for point in custom_polygon:
                if not isinstance(point, (list, tuple)) or len(point) != 2:
                    raise ValueError(
                        f"{spec_name} custom_polygon points must be (x, y) tuples"
                    )

        # Validate color
        color = spec.get("color")
        if color is not None:
            parse_color(color)

        # Validate length
        length = spec.get("length")
        if length is not None:
            if not isinstance(length, (int, float)) or length <= 0 or length > 1:
                raise ValueError(f"{spec_name} length must be a number between 0 and 1")

        # Validate width
        width = spec.get("width")
        if width is not None:
            if not isinstance(width, (int, float)) or width <= 0:
                raise ValueError(f"{spec_name} width must be a positive number")

    def _validate_pivot_spec(self, spec: Dict[str, Any]) -> None:
        """Validate pivot specification dictionary."""
        # Validate shape
        shape = spec.get("shape", "circle")
        if shape not in ["circle"]:
            raise ValueError("pivot_spec shape must be 'circle'")

        # Validate color
        color = spec.get("color")
        if color is not None:
            parse_color(color)

        # Validate radius
        radius = spec.get("radius")
        if radius is not None:
            if not isinstance(radius, (int, float)) or radius <= 0:
                raise ValueError("pivot_spec radius must be a positive number")

    def draw(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        scale_factor: float = 1.0,
    ) -> None:
        """Draw the clock hands.

        Args:
            image: The PIL Image to draw on.
            draw: The PIL ImageDraw object for drawing operations.
            center: The (x, y) center point of the clock face (already scaled).
            radius: The radius of the clock face (already scaled).
            scale_factor: Scale factor for custom element positioning.
        """
        # Use element's own center and radius if specified
        element_center = self.get_center(center, scale_factor)
        element_radius = self.get_radius(radius, scale_factor)

        time_str = self.get_property("time", "12:00:00")
        mode = self.get_property("mode", "12h")

        # Parse time
        try:
            hours, minutes, seconds = validate_time_format(time_str)

            # For 24h mode, hour hand moves through full 360° in 24 hours
            if mode == "24h":
                hour_angle, minute_angle, second_angle = time_to_angles(
                    hours, minutes, seconds, mode_24h=True
                )
            else:
                hour_angle, minute_angle, second_angle = time_to_angles(
                    hours, minutes, seconds
                )
        except ValueError as e:
            print(f"Warning: Invalid time format '{time_str}': {e}")
            hour_angle = minute_angle = second_angle = 0

        # Check for new flexible hands format
        hands = self.get_property("hands")
        if hands:
            for hand in hands:
                hand_type = hand.get("type", "hour")
                if hand_type == "hour":
                    angle = hour_angle
                elif hand_type == "minute":
                    angle = minute_angle
                elif hand_type == "second":
                    angle = second_angle
                else:
                    angle = 0
                self._draw_hand(
                    draw, element_center, element_radius, angle, hand, hand_type
                )
        else:
            # Legacy format: hour_spec, minute_spec, second_spec
            # Draw hands in order: hour, minute, second (second on top)
            hour_spec = self.get_property("hour_spec")
            if hour_spec:
                self._draw_hand(
                    draw, element_center, element_radius, hour_angle, hour_spec, "hour"
                )

            minute_spec = self.get_property("minute_spec")
            if minute_spec:
                self._draw_hand(
                    draw,
                    element_center,
                    element_radius,
                    minute_angle,
                    minute_spec,
                    "minute",
                )

            second_spec = self.get_property("second_spec")
            if second_spec:
                self._draw_hand(
                    draw,
                    element_center,
                    element_radius,
                    second_angle,
                    second_spec,
                    "second",
                )

        # Draw pivot on top of all hands
        pivot_spec = self.get_property("pivot_spec")
        if pivot_spec:
            self._draw_pivot(draw, center, pivot_spec)

    def _draw_hand(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        angle: float,
        spec: Dict[str, Any],
        hand_type: str,
    ) -> None:
        """Draw a single hand."""
        shape = spec.get("shape", "line")
        color = parse_color(spec.get("color", "black"))
        length = spec.get("length", 0.6) * radius
        width = spec.get("width", 2)

        if shape == "line":
            self._draw_line_hand(draw, center, angle, length, width, color)
        elif shape == "triangle":
            self._draw_triangle_hand(draw, center, angle, length, width, color)
        elif shape == "custom_polygon":
            custom_polygon = spec.get("custom_polygon", [])
            self._draw_custom_hand(
                draw, center, angle, length, width, color, custom_polygon
            )

    def _draw_line_hand(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        angle: float,
        length: float,
        width: float,
        color: Any,
    ) -> None:
        """Draw a simple line hand."""
        end_point = point_on_circle(center, length, angle)
        draw.line([center, end_point], fill=color, width=int(width))

    def _draw_triangle_hand(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        angle: float,
        length: float,
        width: float,
        color: Any,
    ) -> None:
        """Draw a triangular hand."""
        # Calculate triangle points
        tip = point_on_circle(center, length, angle)

        # Base points perpendicular to hand direction
        base_offset = width / 2
        left_base = point_on_circle(center, base_offset, angle - 90)
        right_base = point_on_circle(center, base_offset, angle + 90)

        # Draw filled triangle
        points = [tip, left_base, right_base]
        draw.polygon(points, fill=color)

    def _draw_custom_hand(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        angle: float,
        length: float,
        width: float,
        color: Any,
        custom_polygon: List[Tuple[float, float]],
    ) -> None:
        """Draw a custom polygon hand."""
        if not custom_polygon:
            # Fallback to line if no polygon defined
            self._draw_line_hand(draw, center, angle, length, width, color)
            return

        # Transform polygon points
        # Scale by length and rotate by angle, then translate to center
        angle_rad = math.radians(angle - 90)  # Adjust for clock orientation
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        transformed_points = []
        for x, y in custom_polygon:
            # Scale by length
            scaled_x = x * length
            scaled_y = y * length

            # Rotate
            rotated_x = scaled_x * cos_a - scaled_y * sin_a
            rotated_y = scaled_x * sin_a + scaled_y * cos_a

            # Translate to center
            final_x = center[0] + rotated_x
            final_y = center[1] + rotated_y

            transformed_points.append((final_x, final_y))

        # Draw filled polygon
        draw.polygon(transformed_points, fill=color)

    def _draw_pivot(
        self,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        spec: Dict[str, Any],
    ) -> None:
        """Draw the central pivot point."""
        shape = spec.get("shape", "circle")
        color = parse_color(spec.get("color", "black"))
        radius = spec.get("radius", 5)

        if shape == "circle":
            # Draw filled circle at center
            bbox = [
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ]
            draw.ellipse(bbox, fill=color)
