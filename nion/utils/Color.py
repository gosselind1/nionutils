from __future__ import annotations

import typing
import re


class Color:
    """This class aims to solve the current usage of strings as a color within Swift.
    It simplifies storage and conversion to enable easy comparisons and other color related operations rather than
    needing to manually deal with strings every time a color is utilized.
    Colors are explicitly based around CSS colors: https://www.w3.org/TR/css-color-4/.
    Internally, swift currently utilizes: <hex-color>, <named-color>, <rgb()> and <rgba()>. Therefore this initial
    implementation targets those formats.
    """

    __SUPPORTED_FUNCTIONS = {"rgb", "rgba"}
    __SUPPORTED_TYPES = {"hex-color", "named-color", "transparent", "rgb", "rgba"}
    __FUNCTION_PATTERN = re.compile(r".+?\(.*\)$")
    # Color list per the css spec
    __NAME_TO_COLOR_TABLE = {"aliceblue": "#f0f8ff", "antiquewhite": "#faebd7", "aqua": "#00ffff",
                             "aquamarine": "#7fffd4", "azure": "#f0ffff", "beige": "#f5f5dc", "bisque": "#ffe4c4",
                             "black": "#000000", "blanchedalmond": "#ffebcd", "blue": "#0000ff",
                             "blueviolet": "#8a2be2", "brown": "#a52a2a", "burlywood": "#deb887",
                             "cadetblue": "#5f9ea0", "chartreuse": "#7fff00", "chocolate": "#d2691e",
                             "coral": "#ff7f50",  "cornflowerblue": "#6495ed", "cornsilk": "#fff8dc",
                             "crimson": "#dc143c", "cyan": "#00ffff", "darkblue": "#00008b", "darkcyan": "#008b8b",
                             "darkgoldenrod": "#b8860b", "darkgray": "#a9a9a9", "darkgreen": "#006400",
                             "darkgrey": "#a9a9a9", "darkkhaki": "#bdb76b", "darkmagenta": "#8b008b",
                             "darkolivegreen": "#556b2f", "darkorange": "#ff8c00", "darkorchid": "#9932cc",
                             "darkred": "#8b0000", "darksalmon": "#e9967a", "darkseagreen": "#8fbc8f",
                             "darkslateblue": "#483d8b", "darkslategray": "#2f4f4f", "darkslategrey": "#2f4f4f",
                             "darkturquoise": "#00ced1", "darkviolet": "#9400d3", "deeppink": "#ff1493",
                             "deepskyblue": "#00bfff", "dimgray": "#696969", "dimgrey": "#696969",
                             "dodgerblue": "#1e90ff",  "firebrick": "#b22222", "floralwhite": "#fffaf0",
                             "forestgreen": "#228b22", "fuchsia": "#ff00ff", "gainsboro": "#dcdcdc",
                             "ghostwhite": "#f8f8ff", "gold": "#ffd700", "goldenrod": "#daa520", "gray": "#808080",
                             "green": "#008000", "greenyellow": "#adff2f", "grey": "#808080", "honeydew": "#f0fff0",
                             "hotpink": "#ff69b4", "indianred": "#cd5c5c", "indigo": "#4b0082", "ivory": "#fffff0",
                             "khaki": "#f0e68c", "lavender": "#e6e6fa", "lavenderblush": "#fff0f5",
                             "lawngreen": "#7cfc00", "lemonchiffon": "#fffacd", "lightblue": "#add8e6",
                             "lightcoral": "#f08080", "lightcyan": "#e0ffff", "lightgoldenrodyellow": "#fafad2",
                             "lightgray": "#d3d3d3", "lightgreen": "#90ee90", "lightgrey": "#d3d3d3",
                             "lightpink": "#ffb6c1", "lightsalmon": "#ffa07a", "lightseagreen": "#20b2aa",
                             "lightskyblue": "#87cefa", "lightslategray": "#778899", "lightslategrey": "#778899",
                             "lightsteelblue": "#b0c4de", "lightyellow": "#ffffe0", "lime": "#00ff00",
                             "limegreen": "#32cd32", "linen": "#faf0e6", "magenta": "#ff00ff", "maroon": "#800000",
                             "mediumaquamarine": "#66cdaa", "mediumblue": "#0000cd", "mediumorchid": "#ba55d3",
                             "mediumpurple": "#9370db", "mediumseagreen": "#3cb371", "mediumslateblue": "#7b68ee",
                             "mediumspringgreen": "#00fa9a", "mediumturquoise": "#48d1cc", "mediumvioletred": "#c71585",
                             "midnightblue": "#191970", "mintcream": "#f5fffa", "mistyrose": "#ffe4e1",
                             "moccasin": "#ffe4b5", "navajowhite": "#ffdead", "navy": "#000080", "oldlace": "#fdf5e6",
                             "olive": "#808000", "olivedrab": "#6b8e23", "orange": "#ffa500", "orangered": "#ff4500",
                             "orchid": "#da70d6", "palegoldenrod": "#eee8aa", "palegreen": "#98fb98",
                             "paleturquoise": "#afeeee", "palevioletred": "#db7093", "papayawhip": "#ffefd5",
                             "peachpuff": "#ffdab9", "peru": "#cd853f", "pink": "#ffc0cb", "plum": "#dda0dd",
                             "powderblue": "#b0e0e6", "purple": "#800080", "rebeccapurple": "#663399", "red": "#ff0000",
                             "rosybrown": "#bc8f8f", "royalblue": "#4169e1", "saddlebrown": "#8b4513",
                             "salmon": "#fa8072", "sandybrown": "#f4a460", "seagreen": "#2e8b57", "seashell": "#fff5ee",
                             "sienna": "#a0522d", "silver": "#c0c0c0", "skyblue": "#87ceeb", "slateblue": "#6a5acd",
                             "slategray": "#708090", "slategrey": "#708090", "snow": "#fffafa",
                             "springgreen": "#00ff7f", "steelblue": "#4682b4", "tan": "#d2b48c", "teal": "#008080",
                             "thistle": "#d8bfd8", "tomato": "#ff6347", "turquoise": "#40e0d0", "violet": "#ee82ee",
                             "wheat": "#f5deb3", "white": "#ffffff", "whitesmoke": "#f5f5f5", "yellow": "#ffff00",
                             "yellowgreen": "#9acd32"}
    __COLOR_TO_NAME_TABLE = {v: k for k, v in __NAME_TO_COLOR_TABLE.items()}

    def __init__(self, color: str) -> None:
        """Initializes a new color object.
        If the given color is invalid, black will be used instead.

        :param str color: A valid CSS color
        """
        self.__stored_color: str = color
        self.__color_type: typing.Optional[str] = None
        self.__color_parameters: typing.Optional[str] = None
        self.__is_function: typing.Optional[bool] = None
        self.__is_valid:typing.Optional[bool] = None

    @property
    def stored_color(self) -> str:
        """Retrieves the originally stored color in the object.
        This property is read-only by design.

        :return: A string of the original inputted color
        """
        return self.__stored_color

    @property
    def color_type(self) -> str:
        """Retrieves the CSS color type of the input color.

        :return: A string of the color type, or "unknown" if the color type is unsupported
        """
        if self.__color_type:
            return self.__color_type

        color = self.stored_color.lower()  # css spec says all functions are treated as lowercase

        if len(color) == 0:
            color_type = "unknown"
        elif self.is_function:
            color_type = color[:color.index("(")]
        elif color[0] == "#":
            color_type = "hex-color"
        elif color in self.__NAME_TO_COLOR_TABLE:
            color_type = "named-color"
        elif color == "transparent":
            color_type = "transparent"
        else:
            color_type = "unknown"

        if color_type not in self.__SUPPORTED_TYPES:
            color_type = "unknown"
        self.__color_type = color_type
        return self.__color_type

    @property
    def is_function(self) -> bool:
        """States if the input color is a function.

        :return: A bool of whether the input color looks like a CSS color function.
        """
        if self.__is_function:
            return self.__is_function

        color = self.stored_color
        self.__is_function = self.__FUNCTION_PATTERN.fullmatch(color) is not None
        return self.__is_function

    @property
    def color_parameters(self) -> str:
        """Retrieves the parameters of the input color.
        If the color is not a function color, it will always return an empty string.

        :return: A string of the input color's function parameters, if applicable.
        """
        if self.__color_parameters:
            return self.__color_parameters

        color = self.stored_color
        if self.is_function:
            color_parameters = color[color.index("(")+1:-1]
        else:
            color_parameters = ""

        self.__color_parameters = color_parameters
        return self.__color_parameters

    @property
    def is_valid(self) -> bool:
        """States whether the input color is a valid color. That is, is it a proper CSS statement.

        :return: A bool of whether the input color string appears valid.
        """
        if self.__is_valid:
            return self.__is_valid

        if self.color_type not in self.__SUPPORTED_TYPES:
            self.__is_valid = False
        elif self.is_function:
            self.__is_valid = self.__validate_function_parameters()
        elif self.color_type == "hex-color":
            self.__is_valid = self.__validate_hex_color()
        else:  # Transparent and named colors get a pass as we determine they are valid during type checking
            self.__is_valid = True

        return self.__is_valid

    def __validate_hex_color(self) -> bool:
        """Determines if the saved color is a valid hex color.
        This function is intended to be called by __is_valid, where it has already been determined that the color this
        function is operating on is in the format of a hex-color.

        :return: A bool of whether the input color is a valid hex color,
        """
        VALID_LENGTHS = {3, 4, 6, 8}
        color = self.stored_color[1:]

        if len(color) not in VALID_LENGTHS:
            return False

        try:
            int(color, 16)
            return True
        except ValueError:
            return False

    def __validate_function_parameters(self) -> bool:
        """This function should be called by is_valid. If a color is determined to be a css color function, this
        function does some initial setup to have a specific function validator check if the color function is valid.

        :return: A bool of whether the given function parameters appear to be valid.
        :raise NotImplementedError: If the given color is an unimplemented function.
        """
        VALIDATORS = {"rgb": Color.__validate_rgb_parameters,
                      "rgba": Color.__validate_rgb_parameters}

        parameters = self.color_parameters
        if "," in self.stored_color:
            try:
                parameters = self.__legacy_parameters_to_modern(parameters)
            except ValueError:
                return False

        if self.color_type not in VALIDATORS:
            raise NotImplementedError("{} parameter validation not implemented".format(self.color_type))
        return VALIDATORS[self.color_type](self)

    def __validate_rgb_parameters(self) -> bool:
        """If a color is determined the be of the rgb/rgba type, this function determines if the function parameters are
        valid. This should be called by __validate_function_parameters.

        :return: A bool of whether the rgb/rgba function signature is correct
        """
        parameters = [parameter for parameter in self.color_parameters.split(" ") if len(parameter)]
        len_parameters = len(parameters)

        if len_parameters < 3:
            return False
        elif len_parameters == 3:
            parameters += "255"
        elif len_parameters == 5:
            if parameters[3] == "/":
                len_parameters -= 2
                del parameters[3]
            else:
                return False  # If the 4th argument isn't /, there's too many arguments
        elif len_parameters >= 6:
            return False  # Too many arguments

        is_percent = parameters[0][-1] == "%"  # check if types are synced
        return all(is_percent == (parameter[-1] == "%") for parameter in parameters[:len_parameters])

    def to_hex_color(self) -> Color:
        """Converts a given color to an equivalent or close to equivalent color in the hex-color format.
        Depending on the format, some lossy conversion might occur.

        :return: A new Color object containing a copy of the original color as a hex-color
        :raise NotImplementedError: If the color object type is unable to be converted to hex.
        """
        HEX_CONVERTERS = {"hex-color": Color.__hex_color_to_hex,
                          "named-color": Color.__named_color_to_hex,
                          "transparent": Color.__transparent_to_hex,
                          "rgb": Color.__rgb_to_hex,
                          "rgba": Color.__rgb_to_hex}

        if self.color_type not in HEX_CONVERTERS:
            raise NotImplementedError("Hex conversion not implemented for {}".format(self.color_type))
        return HEX_CONVERTERS[self.color_type](self)

    def __hex_color_to_hex(self) -> Color:
        """Converts a hex color to a hex color. Intended to be called by to_hex_color.

        :return: A new hex color based on the calling color.
        """
        return Color(self.stored_color)

    def __named_color_to_hex(self) -> Color:
        """Converts a named color to a hex color. Intended to be called by to_hex_color.

        :return: A new hex color based on the calling named color.
        """
        hex_color = self.__NAME_TO_COLOR_TABLE[self.stored_color.lower()]
        return Color(hex_color)

    def __transparent_to_hex(self) -> Color:
        """Converts a transparent color to a hex color. Intended to be called by to_hex_color.

        :return: A new color object with the color of "#00000000"
        """
        return Color("#00000000")

    def __rgb_to_hex(self) -> Color:
        """Converts a rgb(a) color to a hex color. Intended to be called by to_hex_color.

        :return: A new hex color based on the calling color.
        :raise NotImplementedError: If the rgb(a) color cannot be converted to hex.
        """
        if not self.is_valid:
            raise ValueError("Cannot convert invalid rgb color to hex")

        parameters = self.color_parameters
        if "," in parameters:
            parameters = self.__legacy_parameters_to_modern(parameters)

        split_parameters = [parameter for parameter in parameters.split(" ") if len(parameter) > 0]
        if split_parameters[3] == "/":
            del split_parameters[3]
        int_parameters = map(Color.__rgb_color_value_to_eight_bit, split_parameters)
        hex_parameters = map(lambda p: hex(p)[2:], int_parameters)

        hex_color = "#" + "".join(hex_parameters)
        return Color(hex_color)

    def to_expanded_notation(self) -> Color:
        """For any valid color, this function produces a copy of that color expressed in the largest possible notation.

        :return: A new color object representing the calling color in expanded notation.
        :raise NotImplementedError: If the color-type cannot be expanded.
        :raise ValueError: If the color is not valid.
        """
        EXPANDERS = {"hex-color": Color.__hex_color_expander,
                     "rgb": Color.__rgb_color_expander,
                     "rgba": Color.__rgb_color_expander}

        if not self.is_valid:
            raise ValueError("Notation expansion cannot occur on invalid colors")
        if self.color_type not in EXPANDERS:
            raise NotImplementedError("Notation expansion cannot be performed on {}".format(self.color_type))
        return EXPANDERS[self.color_type](self)

    def __hex_color_expander(self) -> Color:
        """Given a color object that is assumed to be a hex-color, this returns a new color object of the extended 9
        character format. This should be called from to_expanded_notation

        :return: A new color object based on the original color object, in extended form.
        """
        color = self.stored_color[1:]

        if len(color) == 3:
            color = color + "F"
        if len(color) == 4:
            color = "".join(c*2 for c in color)
        if len(color) == 6:
            color = color + "FF"

        color = "#" + color
        return Color(color)

    def __rgb_color_expander(self) -> Color:
        """Given a color object that is assumed to be a rgb(a) color, this returns a new color object of the extended
        rgb(a) function call. This applies to both legacy and modern syntax.

        :return: A new color object based on the original color object, in extended form.
        """
        color = self.color_parameters
        is_legacy = "," in color
        if is_legacy:
            color = color.replace(",", " ")
        parameters = [parameter for parameter in color.split(" ") if len(parameter)]

        if len(parameters) == 3:
            parameters.append("255")
        if len(parameters) == 4:
            parameters.insert(3, "/")

        if is_legacy:
            del parameters[3]
            color = ", ".join(parameters)
        else:
            color = " ".join(parameters)

        color = self.color_type + "(" + color + ")"
        return Color(color)

    def without_alpha(self) -> Color:
        """Returns a new copy of the color, without any transparency

        :return: A new Color based on the calling color, without alpha.
        :raise NotImplementedError: If it is not possible to remove alpha while preserving the color format.
        :raise ValueError: If the color is not valid.
        """
        
        ALPHA_REMOVERS = {"hex-color": Color.__hex_without_alpha,
                          "named-color": lambda c: Color(c.stored_color),
                          "rgb": Color.__rgb_without_alpha,
                          "rgba": Color.__rgb_without_alpha}

        if not self.is_valid:
            raise ValueError("{} is not a valid color".format(self.stored_color))
        if self.color_type not in ALPHA_REMOVERS:
            raise NotImplementedError("Alpha removal cannot be performed on {}".format(self.color_type))

        return ALPHA_REMOVERS[self.color_type](self)

    def __hex_without_alpha(self) -> Color:
        """Removes the transparency from a hex-color format color. Should be called from without_alpha.
        This function keeps the output format the same length as the input format.

        :return: A new color based on the calling color, without alpha.
        """
        color = self.stored_color
        if len(color) == 5:
            color = color[:-1] + "F"
        elif len(color) == 9:
            color = color[:-2] + "FF"
        return Color(color)

    def __rgb_without_alpha(self) -> Color:
        """Removes the transparency from a hex-color format color. Should be called from without_alpha.
        This function keeps the output format the same length as the input format.

        :return: A new color based on the calling color, without alpha.
        """
        params = self.color_parameters
        is_legacy = "," in params
        if is_legacy:
            params = Color.__legacy_parameters_to_modern(params)

        split_params = params.split(" ")
        if len(split_params) > 3:
            target_position = len(split_params) - 1
            if split_params[target_position][-1] == "%":
                split_params[target_position] = "100%"
            else:
                split_params[target_position] = "255"

        if is_legacy:
            params = ", ".join(split_params)
        else:
            params = " ".join(split_params)

        assert self.__color_type is not None
        color = self.__color_type + "(" + params + ")"

        return Color(color)

    def __str__(self) -> str:
        """Gives a string representation of the color object.
        This gives the stored_color value, or the original input color string, as a string.

        :return: A str of the input color.
        """
        return str(self.stored_color)

    def __repr__(self) -> str:
        """Gives a representation of the color object.
        This gives the representation of the original input color string.

        :return: A str representation of the input color.
        """
        return repr(self.stored_color)

    def __eq__(self, other: typing.Any) -> bool:
        """Compares two color objects for equality. This is accomplished by converting the colors to hex format,
        and then checking if the colors match. This means for lossless values, there are some overlapping colors due to
        rounding.

        :param other: Another object to compare the color against.
        :return: A bool of whether these colors are a "Close enough" match
        :raise ValueError: If a color is invalid, or improperly formed.
        :raise NotImplementedError: If a color cannot be converted and or expanded.
        """
        if not isinstance(other, Color):
            return False

        color_a = self.to_hex_color().to_expanded_notation()
        color_b = other.to_hex_color().to_expanded_notation()
        return color_a.stored_color == color_b.stored_color

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
    def __rgb_color_value_to_eight_bit(value: str) -> int:
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
            float_value = Color.__css_percent_interpolation(float_value, MIN, MAX)

        int_value = int(round(float_value))
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
