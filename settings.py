from manim import *  # type: ignore


# Recto
RECTO_COLOR_TUPLE: tuple = ("#51da4c", "#ffffff")
RECTO_COLOR_LIST: list = color_gradient(
    (rgb_to_color(hex_to_rgb("#d3cde8")), rgb_to_color(hex_to_rgb("#b5e0ea"))), 8
)  # low rendering time impact
RECTO_HEIGHT: float = 1.0  # rather not to modify this
RECTO_WIDTH_MULTIPLIER_RANGE: tuple = (4.0, 32.0)
RECTO_CURVATURE: float = 1.0  # extreme rendering time impact
RECTO_CURVATURE_RANGE: tuple = (0.0, 1.0)  # do not modify this
SHEEN_FACTOR_RANGE: tuple = (0.1, 0.14)
# SHEEN_FACTOR_RANGE: tuple = (0.0, 0.0)

# RectoChain
RECTO_NUMBER_RANGE: tuple = (
    10,
    64,
)  # medium rendering time impact, influenced by RECTOCHAIN_NUMBER
RECTO_SPAN: float = 4.0
RECTOCHAIN_NUMBER: int = (
    16  # medium rendering time impact, influence RECTO_NUMBER_RANGE
)
RECTOCHAIN_SPAN: float = 6.0

# Frame
FRAME_HEIGHT: float = (
    RECTOCHAIN_SPAN * (RECTOCHAIN_NUMBER - 1) + RECTO_HEIGHT * RECTOCHAIN_NUMBER
)
FRAME_WIDTH: float = FRAME_HEIGHT
FRAME_X_RADIUS: float = FRAME_WIDTH / 2
FRAME_Y_RADIUS: float = FRAME_HEIGHT / 2

# Animation
RUN_TIME: float = 30.0  # medium rendering time impact, in seconds
INTERPOLATION_REFERENCE: float = 128.0
MIN_SHIFT_DISTANCE: float = 64.0
MIN_SHIFT_DISTANCE = (
    INTERPOLATION_REFERENCE / 2
    if MIN_SHIFT_DISTANCE > INTERPOLATION_REFERENCE / 2
    else MIN_SHIFT_DISTANCE
)
BASE_VELOCITY: float = 1.0  # do not modify this
VELOCITY_FACTOR: float = 4.0  # rather not to modify this

# Rendering
BACKGROUNG_COLOR: str = "#000000"
PIXEL_HEIGHT: int = 1000  # medium rendering time impact
PIXEL_WIDTH: int = 1000  # medium rendering time impact
FRAME_RATE: float = 60.0  # medium rendering time impact


if __name__ == "__main__":
    pass
