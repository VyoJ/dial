# Dial Library - Examples Gallery

This folder contains advanced examples showcasing the full capabilities of the dial library.

## Running the Examples

```bash
python examples/showcase.py
```

This will generate 7 impressive clock designs demonstrating various advanced features.

## Generated Examples

### 1. Chronograph (gallery_chronograph.png)
Multi-dial chronograph with three independent sub-dials:
- Main clock showing current time
- Seconds counter sub-dial (top)
- Minutes counter sub-dial (left)
- Hours counter sub-dial (right)
- Gradient background
- Custom positioning for all sub-dials

**Features demonstrated:**
- Custom `center` and `radius` for sub-dials
- Independent time displays on each dial
- Radial gradient background
- Multiple layered elements

### 2. 24-Hour Military Clock (gallery_24hour_military.png)
Full 24-hour military time display:
- Dark military-style theme
- 24 hour divisions
- Both 1-12 and 13-24 numerals
- Inner ring shows military time (13-24) in green
- Hour hand completes full rotation in 24 hours

**Features demonstrated:**
- `mode: "24h"` for hour hand
- `divisions: 24` for tick marks
- `radius_offset` for dual numeral rings
- Custom numeral values (13-24)

### 3. Gradient Masterpiece (gallery_gradient_masterpiece.png)
Stunning radial gradient with classic elements:
- Multi-color radial gradient (pink to deep blue)
- Roman numerals in white
- Golden hands
- Date window overlay at 6 o'clock position
- High-quality rendering

**Features demonstrated:**
- Radial gradient with multiple colors
- Custom gradient center point
- Date window overlay positioning
- Roman numeral system
- High-quality antialiasing

### 4. Dual Ring Clock (gallery_dual_ring.png)
Complex layout with two numeral rings:
- Outer ring: Hour numerals (1-12)
- Inner ring: Minute numerals (5-60 in 5-minute intervals)
- 60 minute tick marks
- Blue hands with red second hand

**Features demonstrated:**
- `radius_offset` for positioning numerals
- Multiple `Numerals` elements with different values
- 60-division tick marks
- Custom color schemes

### 5. Mirrored Clock (gallery_mirrored.png)
Beautiful turquoise gradient with image transformation:
- Turquoise to deep teal radial gradient
- White hands and numerals
- Horizontally flipped final image
- Golden second hand

**Features demonstrated:**
- `post_processing: {"flip_horizontal": True}`
- Image-level transformations
- Radial gradient backgrounds
- Selective numeral display

### 6. Ultra-Minimal Clock (gallery_ultra_minimal.png)
Pure minimalist design philosophy:
- Pure white face
- Only corner numerals (12, 3, 6, 9)
- Thin, subtle tick marks
- Elegant thin hands
- No unnecessary elements

**Features demonstrated:**
- `visible: [12, 3, 6, 9]` for selective numerals
- Minimal styling approach
- Thin line widths for elegance
- Clean, modern aesthetic

### 7. Multi-Timezone World Clock (gallery_multi_timezone.png)
Show multiple time zones simultaneously:
- Large main clock showing local time
- Three smaller sub-dials showing different timezones:
  - NYC (blue, top)
  - London (red, left)
  - Tokyo (green, right)
- Each sub-dial has its own color scheme
- Independent time displays

**Features demonstrated:**
- Complex multi-dial layout (4 independent clocks)
- Custom positioning for all sub-dials
- Color-coded time zones
- Coordinated design across multiple elements
- Largest canvas (700×700) for detail

## Key Features Showcased

All examples demonstrate:

✅ **Advanced Positioning** - Custom `center` and `radius` for any element
✅ **Sub-Dials** - Multiple independent clock faces on one canvas
✅ **24-Hour Mode** - Full 24-hour time display capabilities
✅ **Gradients** - Radial and linear gradient backgrounds
✅ **Overlays** - Date windows and text overlays
✅ **Dual Rings** - Multiple numeral rings using `radius_offset`
✅ **Post-Processing** - Image transformations (flip, rotate)
✅ **High Quality** - Antialiasing and supersampling (`scale_factor: 3`)
✅ **Custom Numerals** - Any values, any system (Arabic, Roman)
✅ **Complex Layouts** - Multiple elements working together

## Code Structure

The `showcase.py` file contains self-contained functions for each example. Each function:
1. Defines a complete configuration dictionary
2. Creates the clock from the configuration
3. Saves the result with a descriptive filename

You can copy any function and modify it to create your own designs.

## Extending the Examples

To create your own advanced clock:

1. Copy one of the example functions as a starting point
2. Modify the configuration dictionary
3. Adjust colors, positions, sizes, and elements
4. Run the script to see your creation

## Configuration Tips

- Use `scale_factor: 3` or `4` for high-quality output
- Sub-dials work best with `radius: 50-80` on a 600×600 canvas
- Position sub-dials ensuring they stay inside the main clock boundary
- For gradients, experiment with different color combinations
- Use `visible` or `values` properties to show only specific numerals
- Layer elements carefully using their implicit z-order

## Technical Notes

All positioning is scale-aware - coordinates refer to the target canvas size, not the internal rendering size. The library automatically handles scaling for antialiasing.

Element z-order (drawing order):
- 0: Face (background)
- 1: Ticks
- 2: Numerals
- 3: Overlays
- 4: Hands

Later elements are drawn on top of earlier ones.
