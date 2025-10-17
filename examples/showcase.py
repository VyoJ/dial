#!/usr/bin/env python3
"""
Dial Library - Advanced Examples Gallery
=========================================

This script demonstrates the full capabilities of the dial library with
technically impressive and complex clock designs:

1. Multi-dial chronographs with sub-complications
2. 24-hour military time displays
3. Gradient backgrounds (radial and linear)
4. Date window overlays
5. Custom numeral positioning and dual rings
6. Image post-processing transformations
7. Multiple independent sub-dials

Run this script to generate a gallery of advanced clock designs.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import dial


def create_chronograph():
    """
    Multi-dial chronograph with three sub-dials.
    Demonstrates custom positioning and independent time displays.
    """
    print("Creating chronograph with sub-dials...")

    config = {
        "width": 600,
        "height": 600,
        "antialias": True,
        "scale_factor": 3,
        "elements": [
            # Main face with gradient
            {
                "type": "Face",
                "properties": {
                    "shape": "circle",
                    "color": {
                        "type": "radial",
                        "colors": ["#ffffff", "#e8e8e8"],
                        "center": [0.5, 0.5],
                    },
                    "border_color": "#333",
                    "border_width": 4,
                },
            },
            # Main hour ticks
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
            # Main numerals
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "color": "black",
                    "font_size": 48,
                    "visible": [12, 3, 6, 9],
                },
            },
            # Sub-dial 1: Seconds counter (top)
            {
                "type": "Face",
                "properties": {
                    "center": [300, 150],
                    "radius": 60,
                    "shape": "circle",
                    "color": "#f0f0f0",
                    "border_color": "#666",
                    "border_width": 2,
                },
            },
            {
                "type": "Ticks",
                "properties": {
                    "center": [300, 150],
                    "radius": 60,
                    "divisions": 60,
                    "hour_spec": {
                        "shape": "line",
                        "color": "#666",
                        "length": 0.1,
                        "width": 1,
                    },
                },
            },
            {
                "type": "Hands",
                "properties": {
                    "center": [300, 150],
                    "radius": 60,
                    "time": "0:0:30",
                    "second_spec": {"color": "#666", "length": 0.8, "width": 2},
                },
            },
            # Sub-dial 2: Minutes counter (left)
            {
                "type": "Face",
                "properties": {
                    "center": [180, 300],
                    "radius": 60,
                    "shape": "circle",
                    "color": "#f0f0f0",
                    "border_color": "#666",
                    "border_width": 2,
                },
            },
            {
                "type": "Numerals",
                "properties": {
                    "center": [180, 300],
                    "radius": 60,
                    "system": "arabic",
                    "values": [15, 30, 45, 60],
                    "color": "#666",
                    "font_size": 24,
                },
            },
            {
                "type": "Hands",
                "properties": {
                    "center": [180, 300],
                    "radius": 60,
                    "time": "0:15:0",
                    "minute_spec": {"color": "#666", "length": 0.7, "width": 2},
                },
            },
            # Sub-dial 3: Hours counter (right)
            {
                "type": "Face",
                "properties": {
                    "center": [420, 300],
                    "radius": 60,
                    "shape": "circle",
                    "color": "#f0f0f0",
                    "border_color": "#666",
                    "border_width": 2,
                },
            },
            {
                "type": "Numerals",
                "properties": {
                    "center": [420, 300],
                    "radius": 60,
                    "system": "arabic",
                    "values": [3, 6, 9, 12],
                    "color": "#666",
                    "font_size": 24,
                },
            },
            {
                "type": "Hands",
                "properties": {
                    "center": [420, 300],
                    "radius": 60,
                    "time": "3:0:0",
                    "hour_spec": {"color": "#666", "length": 0.6, "width": 2},
                },
            },
            # Main clock hands
            {
                "type": "Hands",
                "properties": {
                    "time": "10:10:30",
                    "hour_spec": {"color": "black", "length": 0.5, "width": 8},
                    "minute_spec": {"color": "black", "length": 0.75, "width": 6},
                    "second_spec": {"color": "#c41e3a", "length": 0.85, "width": 2},
                    "pivot_spec": {"shape": "circle", "color": "black", "radius": 8},
                },
            },
        ],
    }

    clock = dial.Clock.from_config(config)
    clock.save("examples/gallery_chronograph.png")
    print("  ✓ Saved gallery_chronograph.png")


def create_24hour_military():
    """
    24-hour military time clock with full 24-hour divisions.
    Shows both 1-12 and 13-24 numerals.
    """
    print("Creating 24-hour military clock...")

    config = {
        "width": 600,
        "height": 600,
        "antialias": True,
        "scale_factor": 3,
        "elements": [
            # Dark military-style face
            {
                "type": "Face",
                "properties": {
                    "shape": "circle",
                    "color": "#1a1a1a",
                    "border_color": "#4a4a4a",
                    "border_width": 3,
                },
            },
            # 24 hour divisions
            {
                "type": "Ticks",
                "properties": {
                    "divisions": 24,
                    "hour_spec": {
                        "shape": "line",
                        "color": "#888",
                        "length": 0.06,
                        "width": 2,
                    },
                },
            },
            # Standard numerals (1-12)
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    "color": "#e0e0e0",
                    "font_size": 42,
                },
            },
            # Military numerals (13-24) - inner ring
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "values": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                    "radius_offset": -0.25,
                    "color": "#00ff00",
                    "font_size": 32,
                },
            },
            # Hands in 24-hour mode
            {
                "type": "Hands",
                "properties": {
                    "time": "18:30:00",
                    "mode": "24h",
                    "hour_spec": {"color": "#00ff00", "length": 0.5, "width": 6},
                    "minute_spec": {"color": "#e0e0e0", "length": 0.75, "width": 4},
                    "second_spec": {"color": "#ff0000", "length": 0.85, "width": 2},
                    "pivot_spec": {"shape": "circle", "color": "#00ff00", "radius": 8},
                },
            },
        ],
    }

    clock = dial.Clock.from_config(config)
    clock.save("examples/gallery_24hour_military.png")
    print("  ✓ Saved gallery_24hour_military.png")


def create_gradient():
    """
    Stunning radial gradient with Roman numerals and date window.
    Demonstrates gradient backgrounds and overlay positioning.
    """
    print("Creating gradient...")

    config = {
        "width": 600,
        "height": 600,
        "antialias": True,
        "scale_factor": 3,
        "elements": [
            # Radial gradient background
            {
                "type": "Face",
                "properties": {
                    "shape": "circle",
                    "color": {
                        "type": "radial",
                        "colors": ["#FFB6C1", "#9370DB", "#4169E1", "#191970"],
                        "center": [0.5, 0.4],
                    },
                    "border_color": "#191970",
                    "border_width": 4,
                },
            },
            # Elegant white ticks
            {
                "type": "Ticks",
                "properties": {
                    "hour_spec": {
                        "shape": "line",
                        "color": "white",
                        "length": 0.08,
                        "width": 3,
                    },
                    "minute_spec": {
                        "shape": "line",
                        "color": "#e0e0e0",
                        "length": 0.04,
                        "width": 1,
                    },
                },
            },
            # Roman numerals
            {
                "type": "Numerals",
                "properties": {
                    "system": "roman",
                    "color": "white",
                    "font_size": 52,
                },
            },
            # Date window
            {
                "type": "Overlay",
                "properties": {
                    "type": "date_window",
                    "position": [300, 420],
                    "date": "2025-10-18",
                    "font_size": 32,
                    "text_color": "#191970",
                    "background_color": "white",
                    "border_color": "#191970",
                    "padding": 8,
                },
            },
            # Golden hands
            {
                "type": "Hands",
                "properties": {
                    "time": "10:10:00",
                    "hour_spec": {"color": "#FFD700", "length": 0.5, "width": 8},
                    "minute_spec": {"color": "#FFD700", "length": 0.75, "width": 6},
                    "second_spec": {"color": "white", "length": 0.85, "width": 2},
                    "pivot_spec": {"shape": "circle", "color": "#FFD700", "radius": 10},
                },
            },
        ],
    }

    clock = dial.Clock.from_config(config)
    clock.save("examples/gallery_gradient.png")
    print("  ✓ Saved gallery_gradient.png")


def create_dual_ring_clock():
    """
    Clock with dual numeral rings - hours outer, minutes inner.
    Demonstrates radius_offset for complex layouts.
    """
    print("Creating dual ring clock...")

    config = {
        "width": 600,
        "height": 600,
        "antialias": True,
        "scale_factor": 3,
        "elements": [
            # Clean white face
            {
                "type": "Face",
                "properties": {
                    "shape": "circle",
                    "color": "white",
                    "border_color": "#333",
                    "border_width": 3,
                },
            },
            # Hour markers
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
            # Minute markers (subtle)
            {
                "type": "Ticks",
                "properties": {
                    "divisions": 60,
                    "hour_spec": {
                        "shape": "line",
                        "color": "#ccc",
                        "length": 0.04,
                        "width": 1,
                    },
                },
            },
            # Outer ring: Hour numerals
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    "radius_offset": 0.0,
                    "color": "black",
                    "font_size": 48,
                },
            },
            # Inner ring: Minute numerals (5-minute intervals)
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "values": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
                    "radius_offset": -0.3,
                    "color": "#666",
                    "font_size": 32,
                },
            },
            # Blue hands
            {
                "type": "Hands",
                "properties": {
                    "time": "3:15:45",
                    "hour_spec": {"color": "#0066cc", "length": 0.5, "width": 8},
                    "minute_spec": {"color": "#0066cc", "length": 0.7, "width": 6},
                    "second_spec": {"color": "#cc0000", "length": 0.85, "width": 2},
                    "pivot_spec": {"shape": "circle", "color": "#0066cc", "radius": 8},
                },
            },
        ],
    }

    clock = dial.Clock.from_config(config)
    clock.save("examples/gallery_dual_ring.png")
    print("  ✓ Saved gallery_dual_ring.png")


def create_mirrored_clock():
    """
    Clock with horizontal flip post-processing.
    Demonstrates image transformation operations.
    """
    print("Creating mirrored clock...")

    config = {
        "width": 500,
        "height": 500,
        "antialias": True,
        "scale_factor": 3,
        "post_processing": {"flip_horizontal": True},
        "elements": [
            # Turquoise gradient
            {
                "type": "Face",
                "properties": {
                    "shape": "circle",
                    "color": {
                        "type": "radial",
                        "colors": ["#40E0D0", "#20B2AA", "#008B8B", "#003333"],
                        "center": [0.5, 0.5],
                    },
                    "border_color": "#003333",
                    "border_width": 3,
                },
            },
            {
                "type": "Ticks",
                "properties": {
                    "hour_spec": {
                        "shape": "line",
                        "color": "white",
                        "length": 0.08,
                        "width": 3,
                    }
                },
            },
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "color": "white",
                    "font_size": 52,
                    "visible": [12, 3, 6, 9],
                },
            },
            {
                "type": "Hands",
                "properties": {
                    "time": "9:15:00",
                    "hour_spec": {"color": "white", "length": 0.5, "width": 8},
                    "minute_spec": {"color": "white", "length": 0.75, "width": 6},
                    "second_spec": {"color": "#FFD700", "length": 0.85, "width": 2},
                    "pivot_spec": {"shape": "circle", "color": "white", "radius": 8},
                },
            },
        ],
    }

    clock = dial.Clock.from_config(config)
    clock.save("examples/gallery_mirrored.png")
    print("  ✓ Saved gallery_mirrored.png")


def create_ultra_minimal():
    """
    Ultra-minimalist design with only essential elements.
    No numerals, subtle ticks, thin hands.
    """
    print("Creating ultra-minimal clock...")

    config = {
        "width": 500,
        "height": 500,
        "antialias": True,
        "scale_factor": 3,
        "elements": [
            # Pure white face with thin border
            {
                "type": "Face",
                "properties": {
                    "shape": "circle",
                    "color": "white",
                    "border_color": "#e0e0e0",
                    "border_width": 1,
                },
            },
            # Only 12, 3, 6, 9 markers
            {
                "type": "Ticks",
                "properties": {
                    "hour_spec": {
                        "shape": "line",
                        "color": "#ccc",
                        "length": 0.05,
                        "width": 1,
                    }
                },
            },
            # Minimal corner numerals
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "visible": [12, 3, 6, 9],
                    "color": "#999",
                    "font_size": 36,
                },
            },
            # Thin, elegant hands
            {
                "type": "Hands",
                "properties": {
                    "time": "10:10:00",
                    "hour_spec": {"color": "#333", "length": 0.5, "width": 3},
                    "minute_spec": {"color": "#333", "length": 0.75, "width": 2},
                    "second_spec": {"color": "#999", "length": 0.85, "width": 1},
                },
            },
        ],
    }

    clock = dial.Clock.from_config(config)
    clock.save("examples/gallery_ultra_minimal.png")
    print("  ✓ Saved gallery_ultra_minimal.png")


def create_multi_timezone():
    """
    Clock showing multiple time zones with independent sub-dials.
    """
    print("Creating multi-timezone world clock...")

    config = {
        "width": 700,
        "height": 700,
        "antialias": True,
        "scale_factor": 3,
        "elements": [
            # Main face
            {
                "type": "Face",
                "properties": {
                    "shape": "circle",
                    "color": "#f5f5f5",
                    "border_color": "#333",
                    "border_width": 3,
                },
            },
            # Main ticks and numerals
            {
                "type": "Ticks",
                "properties": {
                    "hour_spec": {
                        "shape": "line",
                        "color": "black",
                        "length": 0.06,
                        "width": 2,
                    }
                },
            },
            {
                "type": "Numerals",
                "properties": {
                    "system": "arabic",
                    "color": "black",
                    "font_size": 40,
                    "visible": [12, 3, 6, 9],
                },
            },
            # NYC time (top)
            {
                "type": "Face",
                "properties": {
                    "center": [350, 200],
                    "radius": 70,
                    "color": "#e6f3ff",
                    "border_color": "#0066cc",
                    "border_width": 2,
                },
            },
            {
                "type": "Numerals",
                "properties": {
                    "center": [350, 200],
                    "radius": 70,
                    "system": "arabic",
                    "visible": [12, 3, 6, 9],
                    "font_size": 20,
                    "color": "#0066cc",
                },
            },
            {
                "type": "Hands",
                "properties": {
                    "center": [350, 200],
                    "radius": 70,
                    "time": "10:00:00",
                    "hour_spec": {"color": "#0066cc", "length": 0.5, "width": 3},
                    "minute_spec": {"color": "#0066cc", "length": 0.7, "width": 2},
                },
            },
            # London time (left)
            {
                "type": "Face",
                "properties": {
                    "center": [200, 350],
                    "radius": 70,
                    "color": "#ffe6e6",
                    "border_color": "#cc0000",
                    "border_width": 2,
                },
            },
            {
                "type": "Numerals",
                "properties": {
                    "center": [200, 350],
                    "radius": 70,
                    "system": "arabic",
                    "visible": [12, 3, 6, 9],
                    "font_size": 20,
                    "color": "#cc0000",
                },
            },
            {
                "type": "Hands",
                "properties": {
                    "center": [200, 350],
                    "radius": 70,
                    "time": "3:00:00",
                    "hour_spec": {"color": "#cc0000", "length": 0.5, "width": 3},
                    "minute_spec": {"color": "#cc0000", "length": 0.7, "width": 2},
                },
            },
            # Tokyo time (right)
            {
                "type": "Face",
                "properties": {
                    "center": [500, 350],
                    "radius": 70,
                    "color": "#e6ffe6",
                    "border_color": "#00cc00",
                    "border_width": 2,
                },
            },
            {
                "type": "Numerals",
                "properties": {
                    "center": [500, 350],
                    "radius": 70,
                    "system": "arabic",
                    "visible": [12, 3, 6, 9],
                    "font_size": 20,
                    "color": "#00cc00",
                },
            },
            {
                "type": "Hands",
                "properties": {
                    "center": [500, 350],
                    "radius": 70,
                    "time": "12:00:00",
                    "hour_spec": {"color": "#00cc00", "length": 0.5, "width": 3},
                    "minute_spec": {"color": "#00cc00", "length": 0.7, "width": 2},
                },
            },
            # Main clock - local time
            {
                "type": "Hands",
                "properties": {
                    "time": "10:10:30",
                    "hour_spec": {"color": "black", "length": 0.5, "width": 8},
                    "minute_spec": {"color": "black", "length": 0.75, "width": 6},
                    "second_spec": {"color": "#ff0000", "length": 0.85, "width": 2},
                    "pivot_spec": {"shape": "circle", "color": "black", "radius": 10},
                },
            },
        ],
    }

    clock = dial.Clock.from_config(config)
    clock.save("examples/gallery_multi_timezone.png")
    print("  ✓ Saved gallery_multi_timezone.png")


def main():
    """Generate all advanced clock examples."""
    print("\n" + "=" * 70)
    print("DIAL LIBRARY - ADVANCED EXAMPLES GALLERY")
    print("=" * 70 + "\n")

    os.makedirs("examples", exist_ok=True)

    create_chronograph()
    create_24hour_military()
    create_gradient()
    create_dual_ring_clock()
    create_mirrored_clock()
    create_ultra_minimal()
    create_multi_timezone()

    print("\n" + "=" * 70)
    print("✓ ALL EXAMPLES GENERATED SUCCESSFULLY!")
    print("=" * 70)
    print("\nGenerated gallery:")
    print("  1. gallery_chronograph.png - Multi-dial chronograph")
    print("  2. gallery_24hour_military.png - 24-hour military time")
    print("  3. gallery_gradient.png - Radial gradient with date")
    print("  4. gallery_dual_ring.png - Dual numeral rings")
    print("  5. gallery_mirrored.png - Mirrored with post-processing")
    print("  6. gallery_ultra_minimal.png - Ultra-minimalist design")
    print("  7. gallery_multi_timezone.png - Multi-timezone world clock")
    print("\nThese examples showcase:")
    print("  ✓ Custom element positioning (center, radius)")
    print("  ✓ Sub-dials and multi-dial layouts")
    print("  ✓ 24-hour time mode")
    print("  ✓ Gradient backgrounds (radial/linear)")
    print("  ✓ Date window overlays")
    print("  ✓ Dual numeral rings (radius_offset)")
    print("  ✓ Image post-processing (flip, rotate)")
    print("  ✓ Complex color schemes")
    print()


if __name__ == "__main__":
    main()
