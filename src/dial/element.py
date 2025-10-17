"""Base Element class for dial library components."""

from abc import ABC, abstractmethod
from typing import Any

from PIL import Image, ImageDraw


class Element(ABC):
    """Abstract base class for all clock elements.

    Each element represents a drawable component of the clock face and must
    implement the draw method. Elements are rendered in order of their z_order.
    """

    def __init__(self, **properties: Any) -> None:
        """Initialize the element with given properties.

        Args:
            **properties: Arbitrary keyword arguments for element configuration.
        """
        self.properties = properties
        self._validate_properties()

    def get_center(
        self, default_center: tuple[float, float], scale_factor: float = 1.0
    ) -> tuple[float, float]:
        """Get the center position for this element.

        Args:
            default_center: Default center position (usually canvas center, already scaled).
            scale_factor: Scale factor to apply to custom center values (default 1.0).

        Returns:
            The center position as (x, y) tuple.
        """
        center = self.get_property("center")
        if center is None:
            return default_center
        if not isinstance(center, (list, tuple)) or len(center) != 2:
            raise ValueError("center must be a (x, y) tuple or list")
        # Scale custom center coordinates
        return (float(center[0]) * scale_factor, float(center[1]) * scale_factor)

    def get_radius(self, default_radius: float, scale_factor: float = 1.0) -> float:
        """Get the radius for this element.

        Args:
            default_radius: Default radius (usually calculated from canvas, already scaled).
            scale_factor: Scale factor to apply to custom radius values (default 1.0).

        Returns:
            The radius as a float.
        """
        radius = self.get_property("radius")
        if radius is None:
            return default_radius
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("radius must be a positive number")
        # Scale custom radius
        return float(radius) * scale_factor

    @property
    @abstractmethod
    def z_order(self) -> int:
        """Return the rendering order of this element.

        Lower values are drawn first (appear behind higher values).
        """
        pass

    @abstractmethod
    def draw(
        self,
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        center: tuple[float, float],
        radius: float,
        scale_factor: float = 1.0,
    ) -> None:
        """Draw the element onto the image.

        Args:
            image: The PIL Image to draw on.
            draw: The PIL ImageDraw object for drawing operations.
            center: The (x, y) center point of the clock face (already scaled).
            radius: The radius of the clock face (already scaled).
            scale_factor: Scale factor for custom element positioning (default 1.0).
        """
        pass

    def _validate_properties(self) -> None:
        """Validate the properties for this element.

        Subclasses should override this method to implement specific validation.
        Should raise ValueError for invalid properties.
        """
        pass

    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a property value with optional default.

        Args:
            key: The property key to retrieve.
            default: Default value if key is not found.

        Returns:
            The property value or default.
        """
        return self.properties.get(key, default)

    def set_property(self, key: str, value: Any) -> None:
        """Set a property value.

        Args:
            key: The property key to set.
            value: The value to set.
        """
        self.properties[key] = value
        self._validate_properties()
