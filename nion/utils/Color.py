from __future__ import annotations

import typing
from math import ceil


class Color:
    """This class is intended to simplify color handling by moving away from representing colors as strings
    Colors are based around CSS colors, https://www.w3.org/TR/css-color-4/.
    Internally, swift currently utilizes: <hex-color>, <named-color>, <rgb()>, and <rgba()>. Therefore this initial
    implementation targets these formats.
    """

    def __init__(self, color: str) -> None:
        self.r, self.g, self.b, self.a = Color.__resolve_color(color)

    @staticmethod
    def __resolve_color(color: str) -> typing.Tuple[int, int, int, int]:
        """Attempts to resolve the input color to a valid hex value.
        Swift returns black if an invalid color is given, and this function follows that functionality.

        :param str color:  A string (hopefully) containing a valid color format
        :return: A tuple of four digits representing r, g, b, and a respectively, each in the range of 0-255
        """
        components = 0, 0, 0, 0  # Black with no transparency
        color = color.lower()

        color = Color.__NAME_TO_COLOR_TABLE.get(color, color)

        if color[0] == "#":
            try:
                components = Color.__hex_to_components(color)
            except ValueError:
                pass

        elif color[:3] == "rgb":
            try:
                components = Color.__rgb_to_components(color)
            except ValueError:
                pass

        return components

    @staticmethod
    def __hex_to_components(color: str) -> typing.Tuple[int, int, int, int]:
        """Converts a css hex style color string to a tuple of parameters as ints with an alpha channel.

        :param str color: A css style color string following the official hex value format (must be lowercase)
        :return: A tuple of four ints, each containing the decimal representation of two hex digits and representing the r, g, b, and a channels respectively
        :raise ValueError: The provided input is a not a valid hex color
        """
        color_string = color

        if color[0] != "#":
            raise ValueError("Missing #")
        color = color[1:]

        if len(color) <= 4:
            color = ''.join([c * 2 for c in color])
        if len(color) == 6:
            color = "00" + color

        components = tuple(int(color[i:i + 1], 16) for i in range(0, len(color), 2))
        if len(components) != 4:
            raise ValueError("{} is not a valid length".format(color_string))
        components = typing.cast(typing.Tuple[int, int, int, int], components)

        return components

    @staticmethod
    def __rgb_to_components(color: str) -> typing.Tuple[int, int, int, int]:
        """Converts a css rgb(a) function call to its parameters as 8 bit integers, and includes the alpha channel

        :param str color: A css rgb(a) function call, following any legal format.
        :return: A tuple of four ints containing
        :raise ValueError: The provided input is a not a valid hex color
        """

        color = color.replace("rgba(", "", 1)  # rgba is a legacy function, and operates identically to rgb
        color = color.replace("rgb(", "", 1)
        color = color[:-1]

        if "," in color:
            color = Color.__legacy_parameters_to_modern(color)

        # validate parameter amount and syntax
        parameters = [parameter for parameter in color.split(" ") if len(parameter) > 0]
        check_alpha = True
        len_parameters = len(parameters)

        if len_parameters < 3:
            raise ValueError("Invalid amount of arguments")
        elif len_parameters == 3:
            parameters += "0"
        elif len_parameters == 5:
            if parameters[3] == "/":
                parameters[3] = str(Color.__rgb_value_to_eight_bit(parameters.pop()))
                check_alpha = False
            else:
                raise ValueError("Fourth argument is not '/'")
        elif len_parameters >= 6:
            raise ValueError("Invalid amount of arguments")

        len_parameters -= int(not check_alpha)
        is_percent = parameters[0][-1] == "%"
        if not all(is_percent == (parameter[-1] == "%") for parameter in parameters[:len_parameters]):
            raise ValueError("Values are not type synced")

        components = tuple(map(Color.__rgb_value_to_eight_bit, parameters))
        assert len(components) == 4
        components = typing.cast(typing.Tuple[int, int, int, int], components)

        return components

    @staticmethod
    def __legacy_parameters_to_modern(legacy_params: str) -> str:
        """Converts a CSS legacy style function call to the syntax of a modern css call.

        :param legacy_params: A string containing the inner parameters of a CSS function, ex: "33, 33, 33"
        :return: A string in the modern css function call, ex: "33 33 33"
        :raise ValueError: The provided syntax is invalid, ex: 33,,,33,33
        """
        parameters = [parameter for parameter in legacy_params.split(",")]
        if any(map(lambda parameter: len(parameter) == 0, parameters)):
            raise ValueError("{} in not a valid legacy-style call!".format(legacy_params))
        return " ".join(parameters)

    @staticmethod
    def __rgb_value_to_eight_bit(value: str) -> int:
        """Converts a css number or percent as string to a bounded unsigned 8bit integer.

        :param value: Value to convert.
        :return: An integer being in the range of 0 to 255.
        :raise ValueError: The provided value is not a valid CSS number or percent.
        """
        MAX = 255
        MIN = 0

        percent = value[-1] == "%"
        if percent:
            value = value[:-1]
        float_value = float(value)
        if percent:
            float_value = Color.__css_percent_interpolation(percent, MIN, MAX)

        int_value = int(ceil(float_value))
        int_value = min(MAX, int_value)
        int_value = max(MIN, int_value)

        return int_value

    @staticmethod
    def __css_percent_interpolation(p: float, a: float, b: float) -> float:
        """Given a percentage, p, as a value 0 to 1, this function returns a value p% away from a in the direction of b

        :param p: A floating point value as a percent where 1 is 100% and 0 is 0%
        :param a: A floating point value
        :param b: A floating point value
        :return: A floating point value p% away from a in the direction of b
        """
        return (1 - p) * a + p * b

    # per CSS spec
    __NAME_TO_COLOR_TABLE = {"aliceblue": "#f0f8ff",
                          "antiquewhite": "#faebd7",
                          "aqua": "#00ffff",
                          "aquamarine": "#7fffd4",
                          "azure": "#f0ffff",
                          "beige": "#f5f5dc",
                          "bisque": "#ffe4c4",
                          "black": "#000000",
                          "blanchedalmond": "#ffebcd",
                          "blue": "#0000ff",
                          "blueviolet": "#8a2be2",
                          "brown": "#a52a2a",
                          "burlywood": "#deb887",
                          "cadetblue": "#5f9ea0",
                          "chartreuse": "#7fff00",
                          "chocolate": "#d2691e",
                          "coral": "#ff7f50",
                          "cornflowerblue": "#6495ed",
                          "cornsilk": "#fff8dc",
                          "crimson": "#dc143c",
                          "cyan": "#00ffff",
                          "darkblue": "#00008b",
                          "darkcyan": "#008b8b",
                          "darkgoldenrod": "#b8860b",
                          "darkgray": "#a9a9a9",
                          "darkgreen": "#006400",
                          "darkgrey": "#a9a9a9",
                          "darkkhaki": "#bdb76b",
                          "darkmagenta": "#8b008b",
                          "darkolivegreen": "#556b2f",
                          "darkorange": "#ff8c00",
                          "darkorchid": "#9932cc",
                          "darkred": "#8b0000",
                          "darksalmon": "#e9967a",
                          "darkseagreen": "#8fbc8f",
                          "darkslateblue": "#483d8b",
                          "darkslategray": "#2f4f4f",
                          "darkslategrey": "#2f4f4f",
                          "darkturquoise": "#00ced1",
                          "darkviolet": "#9400d3",
                          "deeppink": "#ff1493",
                          "deepskyblue": "#00bfff",
                          "dimgray": "#696969",
                          "dimgrey": "#696969",
                          "dodgerblue": "#1e90ff",
                          "firebrick": "#b22222",
                          "floralwhite": "#fffaf0",
                          "forestgreen": "#228b22",
                          "fuchsia": "#ff00ff",
                          "gainsboro": "#dcdcdc",
                          "ghostwhite": "#f8f8ff",
                          "gold": "#ffd700",
                          "goldenrod": "#daa520",
                          "gray": "#808080",
                          "green": "#008000",
                          "greenyellow": "#adff2f",
                          "grey": "#808080",
                          "honeydew": "#f0fff0",
                          "hotpink": "#ff69b4",
                          "indianred": "#cd5c5c",
                          "indigo": "#4b0082",
                          "ivory": "#fffff0",
                          "khaki": "#f0e68c",
                          "lavender": "#e6e6fa",
                          "lavenderblush": "#fff0f5",
                          "lawngreen": "#7cfc00",
                          "lemonchiffon": "#fffacd",
                          "lightblue": "#add8e6",
                          "lightcoral": "#f08080",
                          "lightcyan": "#e0ffff",
                          "lightgoldenrodyellow": "#fafad2",
                          "lightgray": "#d3d3d3",
                          "lightgreen": "#90ee90",
                          "lightgrey": "#d3d3d3",
                          "lightpink": "#ffb6c1",
                          "lightsalmon": "#ffa07a",
                          "lightseagreen": "#20b2aa",
                          "lightskyblue": "#87cefa",
                          "lightslategray": "#778899",
                          "lightslategrey": "#778899",
                          "lightsteelblue": "#b0c4de",
                          "lightyellow": "#ffffe0",
                          "lime": "#00ff00",
                          "limegreen": "#32cd32",
                          "linen": "#faf0e6",
                          "magenta": "#ff00ff",
                          "maroon": "#800000",
                          "mediumaquamarine": "#66cdaa",
                          "mediumblue": "#0000cd",
                          "mediumorchid": "#ba55d3",
                          "mediumpurple": "#9370db",
                          "mediumseagreen": "#3cb371",
                          "mediumslateblue": "#7b68ee",
                          "mediumspringgreen": "#00fa9a",
                          "mediumturquoise": "#48d1cc",
                          "mediumvioletred": "#c71585",
                          "midnightblue": "#191970",
                          "mintcream": "#f5fffa",
                          "mistyrose": "#ffe4e1",
                          "moccasin": "#ffe4b5",
                          "navajowhite": "#ffdead",
                          "navy": "#000080",
                          "oldlace": "#fdf5e6",
                          "olive": "#808000",
                          "olivedrab": "#6b8e23",
                          "orange": "#ffa500",
                          "orangered": "#ff4500",
                          "orchid": "#da70d6",
                          "palegoldenrod": "#eee8aa",
                          "palegreen": "#98fb98",
                          "paleturquoise": "#afeeee",
                          "palevioletred": "#db7093",
                          "papayawhip": "#ffefd5",
                          "peachpuff": "#ffdab9",
                          "peru": "#cd853f",
                          "pink": "#ffc0cb",
                          "plum": "#dda0dd",
                          "powderblue": "#b0e0e6",
                          "purple": "#800080",
                          "rebeccapurple": "#663399",
                          "red": "#ff0000",
                          "rosybrown": "#bc8f8f",
                          "royalblue": "#4169e1",
                          "saddlebrown": "#8b4513",
                          "salmon": "#fa8072",
                          "sandybrown": "#f4a460",
                          "seagreen": "#2e8b57",
                          "seashell": "#fff5ee",
                          "sienna": "#a0522d",
                          "silver": "#c0c0c0",
                          "skyblue": "#87ceeb",
                          "slateblue": "#6a5acd",
                          "slategray": "#708090",
                          "slategrey": "#708090",
                          "snow": "#fffafa",
                          "springgreen": "#00ff7f",
                          "steelblue": "#4682b4",
                          "tan": "#d2b48c",
                          "teal": "#008080",
                          "thistle": "#d8bfd8",
                          "tomato": "#ff6347",
                          "turquoise": "#40e0d0",
                          "violet": "#ee82ee",
                          "wheat": "#f5deb3",
                          "white": "#ffffff",
                          "whitesmoke": "#f5f5f5",
                          "yellow": "#ffff00",
                          "yellowgreen": "#9acd32",
                          "transparent": "#00000000"}

    __COLOR_TO_NAME_TABLE = {v: k for k, v in __NAME_TO_COLOR_TABLE.items()}
