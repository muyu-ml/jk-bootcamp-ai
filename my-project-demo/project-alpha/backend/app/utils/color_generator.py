"""Color generation utilities."""
import random


def generate_random_color() -> str:
    """
    Generate a random hex color code.

    Returns:
        A hex color string in the format #RRGGBB
    """
    # Generate random RGB values
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Convert to hex format
    return f"#{r:02X}{g:02X}{b:02X}"


# Predefined color palette for tags
PREDEFINED_COLORS = [
    "#3B82F6",  # blue-500
    "#10B981",  # green-500
    "#F59E0B",  # amber-500
    "#EF4444",  # red-500
    "#8B5CF6",  # violet-500
    "#EC4899",  # pink-500
    "#06B6D4",  # cyan-500
    "#84CC16",  # lime-500
]


def get_color_from_palette(index: int = None) -> str:
    """
    Get a color from the predefined palette.

    Args:
        index: Optional index into the palette. If None, returns a random color.

    Returns:
        A hex color string
    """
    if index is not None:
        return PREDEFINED_COLORS[index % len(PREDEFINED_COLORS)]
    return random.choice(PREDEFINED_COLORS)
