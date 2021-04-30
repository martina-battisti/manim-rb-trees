"""
Constant definitions.
"""

import typing
import os
import numpy as np

# Messages
NOT_SETTING_FONT_MSG: str = """
You haven't set font.
If you are not using English, this may cause text rendering problem.
You set font like:
text = Text('your text', font='your font')
"""
SCENE_NOT_FOUND_MESSAGE: str = """
   {} is not in the script
"""
CHOOSE_NUMBER_MESSAGE: str = """
Choose number corresponding to desired scene/arguments.
(Use comma separated list for multiple entries)
Choice(s): """
INVALID_NUMBER_MESSAGE: str = "Invalid scene numbers have been specified. Aborting."
NO_SCENE_MESSAGE: str = """
   There are no scenes inside that module
"""
HELP_MESSAGE: str = """
   Usage:
   python extract_scene.py <module> [<scene name>]
   -p preview in low quality
   -s show and save picture of last frame
   -w write result to file [this is default if nothing else is stated]
   -o <file_name> write to a different file_name
   -l use low quality
   -m use medium quality
   -a run and save every scene in the script, or all args for the given scene
   -q don't print progress
   -f when writing to a movie file, export the frames in png sequence
   -t use transperency when exporting images
   -n specify the number of the animation to start from
   -r specify a resolution
   -c specify a background color
"""

# Cairo and Pango stuff
NORMAL: str = "NORMAL"
ITALIC: str = "ITALIC"
OBLIQUE: str = "OBLIQUE"
BOLD: str = "BOLD"
# Only for Pango from below
THIN: str = "THIN"
ULTRALIGHT: str = "ULTRALIGHT"
LIGHT: str = "LIGHT"
SEMILIGHT: str = "SEMILIGHT"
BOOK: str = "BOOK"
MEDIUM: str = "MEDIUM"
SEMIBOLD: str = "SEMIBOLD"
ULTRABOLD: str = "ULTRABOLD"
HEAVY: str = "HEAVY"
ULTRAHEAVY: str = "ULTRAHEAVY"

TEX_USE_CTEX = False
TEX_TEXT_TO_REPLACE = "YourTextHere"
TEMPLATE_TEX_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "tex_template.tex" if not TEX_USE_CTEX else "ctex_template.tex"
)
with open(TEMPLATE_TEX_FILE, "r") as infile:
    TEMPLATE_TEXT_FILE_BODY = infile.read()
    TEMPLATE_TEX_FILE_BODY = TEMPLATE_TEXT_FILE_BODY.replace(
        TEX_TEXT_TO_REPLACE,
        "\\begin{align*}\n" + TEX_TEXT_TO_REPLACE + "\n\\end{align*}",
    )

# There might be other configuration than pixel shape later...
PRODUCTION_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 1440,
    "pixel_width": 2560,
    "frame_rate": 60,
}

HIGH_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 1080,
    "pixel_width": 1920,
    "frame_rate": 60,
}

MEDIUM_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 720,
    "pixel_width": 1280,
    "frame_rate": 30,
}

LOW_QUALITY_CAMERA_CONFIG = {
    "pixel_height": 480,
    "pixel_width": 854,
    "frame_rate": 15,
}

# Misc
DEFAULT_POINT_DENSITY_2D: int = 25
DEFAULT_POINT_DENSITY_1D: int = 10
DEFAULT_STROKE_WIDTH: int = 4

DEFAULT_PIXEL_HEIGHT = PRODUCTION_QUALITY_CAMERA_CONFIG["pixel_height"]
DEFAULT_PIXEL_WIDTH = PRODUCTION_QUALITY_CAMERA_CONFIG["pixel_width"]
DEFAULT_FRAME_RATE = 60

FRAME_HEIGHT = 8.0
FRAME_WIDTH = FRAME_HEIGHT * DEFAULT_PIXEL_WIDTH / DEFAULT_PIXEL_HEIGHT
FRAME_Y_RADIUS = FRAME_HEIGHT / 2
FRAME_X_RADIUS = FRAME_WIDTH / 2

# Geometry: directions
ORIGIN: np.ndarray = np.array((0.0, 0.0, 0.0))
"""The center of the coordinate system."""

UP: np.ndarray = np.array((0.0, 1.0, 0.0))
"""One unit step in the positive Y direction."""

DOWN: np.ndarray = np.array((0.0, -1.0, 0.0))
"""One unit step in the negative Y direction."""

RIGHT: np.ndarray = np.array((1.0, 0.0, 0.0))
"""One unit step in the positive X direction."""

LEFT: np.ndarray = np.array((-1.0, 0.0, 0.0))
"""One unit step in the negative X direction."""

IN: np.ndarray = np.array((0.0, 0.0, -1.0))
"""One unit step in the negative Z direction."""

OUT: np.ndarray = np.array((0.0, 0.0, 1.0))
"""One unit step in the positive Z direction."""

# Geometry: axes
X_AXIS: np.ndarray = np.array((1.0, 0.0, 0.0))
Y_AXIS: np.ndarray = np.array((0.0, 1.0, 0.0))
Z_AXIS: np.ndarray = np.array((0.0, 0.0, 1.0))

# Geometry: useful abbreviations for diagonals
UL: np.ndarray = UP + LEFT
"""One step up plus one step left."""

UR: np.ndarray = UP + RIGHT
"""One step up plus one step right."""

DL: np.ndarray = DOWN + LEFT
"""One step down plus one step left."""

DR: np.ndarray = DOWN + RIGHT
"""One step down plus one step right."""

TOP = FRAME_Y_RADIUS * UP
BOTTOM = FRAME_Y_RADIUS * DOWN
LEFT_SIDE = FRAME_X_RADIUS * LEFT
RIGHT_SIDE = FRAME_X_RADIUS * RIGHT

# Geometry
START_X: int = 30
START_Y: int = 20
DEFAULT_DOT_RADIUS = 0.08
DEFAULT_SMALL_DOT_RADIUS = 0.04
DEFAULT_DASH_LENGTH = 0.05
DEFAULT_ARROW_TIP_LENGTH = 0.35

# Default buffers (padding)
SMALL_BUFF: float = 0.1
MED_SMALL_BUFF: float = 0.25
MED_LARGE_BUFF: float = 0.5
LARGE_BUFF: float = 1
DEFAULT_MOBJECT_TO_EDGE_BUFFER: float = MED_LARGE_BUFF
DEFAULT_MOBJECT_TO_MOBJECT_BUFFER: float = MED_SMALL_BUFF

# Times in seconds
DEFAULT_POINTWISE_FUNCTION_RUN_TIME: float = 3.0
DEFAULT_WAIT_TIME: float = 1.0





# Mathematical constants
PI: float = np.pi
"""The ratio of the circumference of a circle to its diameter."""

TAU: float = 2 * PI
"""The ratio of the circumference of a circle to its radius."""

DEGREES: float = TAU / 360
"""The exchange rate between radians and degrees."""

# ffmpeg stuff
FFMPEG_BIN: str = "ffmpeg"

# gif stuff
GIF_FILE_EXTENSION: str = ".gif"

FFMPEG_VERBOSITY_MAP: typing.Dict[str, str] = {
    "DEBUG": "error",
    "INFO": "error",
    "WARNING": "error",
    "ERROR": "error",
    "CRITICAL": "fatal",
}
VERBOSITY_CHOICES = FFMPEG_VERBOSITY_MAP.keys()
WEBGL_RENDERER_INFO: str = (
    "The Electron frontend to Manim is hosted at "
    "https://github.com/ManimCommunity/manim-renderer. After cloning and building it, "
    "you can either start it prior to running Manim or specify the path to the "
    "executable with the --webgl_renderer_path flag."
)

# Video qualities
QUALITIES: typing.Dict[str, typing.Dict[str, typing.Union[str, int, None]]] = {
    "fourk_quality": {
        "flag": "k",
        "pixel_height": 2160,
        "pixel_width": 3840,
        "frame_rate": 60,
    },
    "production_quality": {
        "flag": "p",
        "pixel_height": 1440,
        "pixel_width": 2560,
        "frame_rate": 60,
    },
    "high_quality": {
        "flag": "h",
        "pixel_height": 1080,
        "pixel_width": 1920,
        "frame_rate": 60,
    },
    "medium_quality": {
        "flag": "m",
        "pixel_height": 720,
        "pixel_width": 1280,
        "frame_rate": 30,
    },
    "low_quality": {
        "flag": "l",
        "pixel_height": 480,
        "pixel_width": 854,
        "frame_rate": 15,
    },
    "example_quality": {
        "flag": None,
        "pixel_height": 480,
        "pixel_width": 854,
        "frame_rate": 30,
    },
}

DEFAULT_QUALITY: str = "high_quality"
DEFAULT_QUALITY_SHORT = QUALITIES[DEFAULT_QUALITY]["flag"]

EPILOG = "Made with <3 by Manim Community developers."
HELP_OPTIONS = ["-h", "--help"]
CONTEXT_SETTINGS = {"help_option_names": HELP_OPTIONS}
SHIFT_VALUE = 65505
CTRL_VALUE = 65507

# Colors
COLOR_MAP = {
    "DARK_BLUE": "#236B8E",
    "DARK_BROWN": "#8B4513",
    "LIGHT_BROWN": "#CD853F",
    "BLUE_E": "#1C758A",
    "BLUE_D": "#29ABCA",
    "BLUE_C": "#58C4DD",
    "BLUE_B": "#9CDCEB",
    "BLUE_A": "#C7E9F1",
    "TEAL_E": "#49A88F",
    "TEAL_D": "#55C1A7",
    "TEAL_C": "#5CD0B3",
    "TEAL_B": "#76DDC0",
    "TEAL_A": "#ACEAD7",
    "GREEN_E": "#699C52",
    "GREEN_D": "#77B05D",
    "GREEN_C": "#83C167",
    "GREEN_B": "#A6CF8C",
    "GREEN_A": "#C9E2AE",
    "YELLOW_E": "#E8C11C",
    "YELLOW_D": "#F4D345",
    "YELLOW_C": "#FFFF00",
    "YELLOW_B": "#FFEA94",
    "YELLOW_A": "#FFF1B6",
    "GOLD_E": "#C78D46",
    "GOLD_D": "#E1A158",
    "GOLD_C": "#F0AC5F",
    "GOLD_B": "#F9B775",
    "GOLD_A": "#F7C797",
    "RED_E": "#CF5044",
    "RED_D": "#E65A4C",
    "RED_C": "#FC6255",
    "RED_B": "#FF8080",
    "RED_A": "#F7A1A3",
    "MAROON_E": "#94424F",
    "MAROON_D": "#A24D61",
    "MAROON_C": "#C55F73",
    "MAROON_B": "#EC92AB",
    "MAROON_A": "#ECABC1",
    "PURPLE_E": "#644172",
    "PURPLE_D": "#715582",
    "PURPLE_C": "#9A72AC",
    "PURPLE_B": "#B189C6",
    "PURPLE_A": "#CAA3E8",
    "WHITE": "#FFFFFF",
    "BLACK": "#000000",
    "LIGHT_GRAY": "#BBBBBB",
    "LIGHT_GREY": "#BBBBBB",
    "GRAY": "#888888",
    "GREY": "#888888",
    "DARK_GREY": "#444444",
    "DARK_GRAY": "#444444",
    "DARKER_GREY": "#222222",
    "DARKER_GRAY": "#222222",
    "GREY_BROWN": "#736357",
    "PINK": "#D147BD",
    "LIGHT_PINK": "#DC75CD",
    "GREEN_SCREEN": "#00FF00",
    "ORANGE": "#FF862F",
    #new colors
    "NEW_RED": "#ff2e2e",
    "NEW_RED_STROKE": "#750003",
    "NEW_BLACK_STROKE": "#4d4d4d",

}
PALETTE = list(COLOR_MAP.values())
locals().update(COLOR_MAP)
for name in [s for s in list(COLOR_MAP.keys()) if s.endswith("_C")]:
    locals()[name.replace("_C", "")] = locals()[name]
