"""Face element for clock background and border."""

from typing import Any, Tuple

from PIL import Image, ImageDraw

from dial.element import Element
from dial.utils import create_gradient_image, parse_color


class Face(Element):
    """Clock face background element.

    The Face element provides the background and border for the clock.
    It supports solid colors, gradients, and image backgrounds.
    """

    @property
    def z_order(self) -> int:
        """Face is drawn first (behind all other elements)."""
        return 0

    def _validate_properties(self) -> None:
        """Validate Face element properties."""
        shape = self.get_property("shape", "circle")
        if shape not in ["circle", "square", "rectangle"]:
            raise ValueError(
                f"Invalid shape: {shape}. Must be 'circle', 'square', or 'rectangle'"
            )

        # Validate color if provided
        color = self.get_property("color")
        if color is not None:
            parse_color(color)  # Will raise ValueError if invalid

        # Validate border properties
        border_width = self.get_property("border_width", 0)
        if not isinstance(border_width, (int, float)) or border_width < 0:
            raise ValueError("border_width must be a non-negative number")

        border_color = self.get_property("border_color")
        if border_color is not None and border_width > 0:
            parse_color(border_color)  # Will raise ValueError if invalid

        # Validate image_path if provided
        image_path = self.get_property("image_path")
        if image_path is not None:
            if not isinstance(image_path, str):
                raise ValueError("image_path must be a string")

    def draw(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        center: Tuple[float, float],
        radius: float,
        scale_factor: float = 1.0,
    ) -> None:
        """Draw the face element.

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

        cx, cy = element_center
        shape = self.get_property("shape", "circle")
        color = self.get_property("color", "white")
        border_color = self.get_property("border_color")
        border_width = self.get_property("border_width", 0)
        image_path = self.get_property("image_path")

        # Calculate shape bounds
        if shape == "circle":
            bbox = [
                cx - element_radius,
                cy - element_radius,
                cx + element_radius,
                cy + element_radius,
            ]
        elif shape == "square":
            bbox = [
                cx - element_radius,
                cy - element_radius,
                cx + element_radius,
                cy + element_radius,
            ]
        else:  # rectangle
            # Use full image dimensions for rectangle
            bbox = [0, 0, image.width, image.height]

        # Draw background
        if image_path:
            self._draw_image_background(image, bbox, image_path, shape)
        else:
            self._draw_color_background(image, draw, bbox, color, shape)

        # Draw border if specified
        if border_width > 0 and border_color:
            self._draw_border(draw, bbox, border_color, border_width, shape)

    def _draw_color_background(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        bbox: list,
        color: Any,
        shape: str,
    ) -> None:
        """Draw solid color or gradient background."""
        if isinstance(color, dict):
            # Gradient background
            if shape == "circle":
                # Create gradient on a square and then mask it to circle
                size = int(bbox[2] - bbox[0])
                gradient_img = create_gradient_image((size, size), color)

                # Create circular mask
                mask = Image.new("L", (size, size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, size, size], fill=255)

                # Apply mask and paste onto main image
                gradient_img.putalpha(mask)
                image.paste(gradient_img, (int(bbox[0]), int(bbox[1])), gradient_img)
            else:
                # Rectangle/square gradient
                width = int(bbox[2] - bbox[0])
                height = int(bbox[3] - bbox[1])
                gradient_img = create_gradient_image((width, height), color)
                image.paste(gradient_img, (int(bbox[0]), int(bbox[1])))
        else:
            # Solid color background
            parsed_color = parse_color(color)
            if shape == "circle":
                draw.ellipse(bbox, fill=parsed_color)
            else:
                draw.rectangle(bbox, fill=parsed_color)

    def _draw_image_background(
        self, image: Image.Image, bbox: list, image_path: str, shape: str
    ) -> None:
        """Draw image background."""
        try:
            bg_image = Image.open(image_path)

            # Resize to fit the shape
            width = int(bbox[2] - bbox[0])
            height = int(bbox[3] - bbox[1])

            if shape == "circle":
                # For circle, make it square
                size = min(width, height)
                bg_image = bg_image.resize((size, size), Image.Resampling.LANCZOS)

                # Create circular mask
                mask = Image.new("L", (size, size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, size, size], fill=255)

                # Apply mask
                bg_image.putalpha(mask)

                # Center the circular image
                x_offset = int(bbox[0] + (width - size) / 2)
                y_offset = int(bbox[1] + (height - size) / 2)
                image.paste(bg_image, (x_offset, y_offset), bg_image)
            else:
                # Rectangle/square
                bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
                image.paste(bg_image, (int(bbox[0]), int(bbox[1])))

        except Exception as e:
            # Fallback to white background if image loading fails
            print(f"Warning: Failed to load background image {image_path}: {e}")
            draw = ImageDraw.Draw(image)
            if shape == "circle":
                draw.ellipse(bbox, fill="white")
            else:
                draw.rectangle(bbox, fill="white")

    def _draw_border(
        self,
        draw: ImageDraw.ImageDraw,
        bbox: list,
        border_color: str,
        border_width: float,
        shape: str,
    ) -> None:
        """Draw border around the face."""
        parsed_color = parse_color(border_color)

        if shape == "circle":
            # Draw circle border
            # Adjust bbox for border width
            adjusted_bbox = [
                bbox[0] + border_width / 2,
                bbox[1] + border_width / 2,
                bbox[2] - border_width / 2,
                bbox[3] - border_width / 2,
            ]
            draw.ellipse(adjusted_bbox, outline=parsed_color, width=int(border_width))
        else:
            # Draw rectangle border
            adjusted_bbox = [
                bbox[0] + border_width / 2,
                bbox[1] + border_width / 2,
                bbox[2] - border_width / 2,
                bbox[3] - border_width / 2,
            ]
            draw.rectangle(adjusted_bbox, outline=parsed_color, width=int(border_width))
