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
    ) -> None:
        """Draw the element onto the image.

        Args:
            image: The PIL Image to draw on.
            draw: The PIL ImageDraw object for drawing operations.
            center: The (x, y) center point of the clock face.
            radius: The radius of the clock face.
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
