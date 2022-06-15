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
    __NAME_TO_COLOR_TABLE = {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', 'aqua': '#00FFFF',
                             'aquamarine': '#7FFFD4', 'azure': '#F0FFFF', 'beige': '#F5F5DC', 'bisque': '#FFE4C4',
                             'black': '#000000', 'blanchedalmond': '#FFEBCD', 'blue': '#0000FF',
                             'blueviolet': '#8A2BE2', 'brown': '#A52A2A', 'burlywood': '#DEB887',
                             'cadetblue': '#5F9EA0', 'chartreuse': '#7FFF00', 'chocolate': '#D2691E',
                             'coral': '#FF7F50', 'cornflowerblue': '#6495ED', 'cornsilk': '#FFF8DC',
                             'crimson': '#DC143C', 'cyan': '#00FFFF', 'darkblue': '#00008B', 'darkcyan': '#008B8B',
                             'darkgoldenrod': '#B8860B', 'darkgray': '#A9A9A9', 'darkgreen': '#006400',
                             'darkgrey': '#A9A9A9', 'darkkhaki': '#BDB76B', 'darkmagenta': '#8B008B',
                             'darkolivegreen': '#556B2F', 'darkorange': '#FF8C00', 'darkorchid': '#9932CC',
                             'darkred': '#8B0000', 'darksalmon': '#E9967A', 'darkseagreen': '#8FBC8F',
                             'darkslateblue': '#483D8B', 'darkslategray': '#2F4F4F', 'darkslategrey': '#2F4F4F',
                             'darkturquoise': '#00CED1', 'darkviolet': '#9400D3', 'deeppink': '#FF1493',
                             'deepskyblue': '#00BFFF', 'dimgray': '#696969', 'dimgrey': '#696969',
                             'dodgerblue': '#1E90FF', 'firebrick': '#B22222', 'floralwhite': '#FFFAF0',
                             'forestgreen': '#228B22', 'fuchsia': '#FF00FF', 'gainsboro': '#DCDCDC',
                             'ghostwhite': '#F8F8FF', 'gold': '#FFD700', 'goldenrod': '#DAA520', 'gray': '#808080',
                             'green': '#008000', 'greenyellow': '#ADFF2F', 'grey': '#808080', 'honeydew': '#F0FFF0',
                             'hotpink': '#FF69B4', 'indianred': '#CD5C5C', 'indigo': '#4B0082', 'ivory': '#FFFFF0',
                             'khaki': '#F0E68C', 'lavender': '#E6E6FA', 'lavenderblush': '#FFF0F5',
                             'lawngreen': '#7CFC00', 'lemonchiffon': '#FFFACD', 'lightblue': '#ADD8E6',
                             'lightcoral': '#F08080', 'lightcyan': '#E0FFFF', 'lightgoldenrodyellow': '#FAFAD2',
                             'lightgray': '#D3D3D3', 'lightgreen': '#90EE90', 'lightgrey': '#D3D3D3',
                             'lightpink': '#FFB6C1', 'lightsalmon': '#FFA07A', 'lightseagreen': '#20B2AA',
                             'lightskyblue': '#87CEFA', 'lightslategray': '#778899', 'lightslategrey': '#778899',
                             'lightsteelblue': '#B0C4DE', 'lightyellow': '#FFFFE0', 'lime': '#00FF00',
                             'limegreen': '#32CD32', 'linen': '#FAF0E6', 'magenta': '#FF00FF', 'maroon': '#800000',
                             'mediumaquamarine': '#66CDAA', 'mediumblue': '#0000CD', 'mediumorchid': '#BA55D3',
                             'mediumpurple': '#9370DB', 'mediumseagreen': '#3CB371', 'mediumslateblue': '#7B68EE',
                             'mediumspringgreen': '#00FA9A', 'mediumturquoise': '#48D1CC', 'mediumvioletred': '#C71585',
                             'midnightblue': '#191970', 'mintcream': '#F5FFFA', 'mistyrose': '#FFE4E1',
                             'moccasin': '#FFE4B5', 'navajowhite': '#FFDEAD', 'navy': '#000080', 'oldlace': '#FDF5E6',
                             'olive': '#808000', 'olivedrab': '#6B8E23', 'orange': '#FFA500', 'orangered': '#FF4500',
                             'orchid': '#DA70D6', 'palegoldenrod': '#EEE8AA', 'palegreen': '#98FB98',
                             'paleturquoise': '#AFEEEE', 'palevioletred': '#DB7093', 'papayawhip': '#FFEFD5',
                             'peachpuff': '#FFDAB9', 'peru': '#CD853F', 'pink': '#FFC0CB', 'plum': '#DDA0DD',
                             'powderblue': '#B0E0E6', 'purple': '#800080', 'rebeccapurple': '#663399', 'red': '#FF0000',
                             'rosybrown': '#BC8F8F', 'royalblue': '#4169E1', 'saddlebrown': '#8B4513',
                             'salmon': '#FA8072', 'sandybrown': '#F4A460', 'seagreen': '#2E8B57', 'seashell': '#FFF5EE',
                             'sienna': '#A0522D', 'silver': '#C0C0C0', 'skyblue': '#87CEEB', 'slateblue': '#6A5ACD',
                             'slategray': '#708090', 'slategrey': '#708090', 'snow': '#FFFAFA',
                             'springgreen': '#00FF7F', 'steelblue': '#4682B4', 'tan': '#D2B48C', 'teal': '#008080',
                             'thistle': '#D8BFD8', 'tomato': '#FF6347', 'turquoise': '#40E0D0', 'violet': '#EE82EE',
                             'wheat': '#F5DEB3', 'white': '#FFFFFF', 'whitesmoke': '#F5F5F5', 'yellow': '#FFFF00',
                             'yellowgreen': '#9ACD32'}
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
        """If a color is determined to be of the rgb/rgba type, this function determines if the function parameters are
        valid. This should be called by __validate_function_parameters.

        :return: A bool of whether the rgb/rgba function signature is correct
        """
        parameters = self.color_parameters

        if "," in parameters:
            split_parameters = [parameter for parameter in self.__legacy_parameters_to_modern(parameters).split(" ") if len(parameter)]
            if len(parameters.replace(" ", "").split(",")) != len(split_parameters):
                return False
        else:
            split_parameters = [parameter for parameter in parameters.split(" ") if len(parameter)]

        parameter_count = len(split_parameters)
        if parameter_count < 3:
            return False
        elif parameter_count == 5:
            if split_parameters[3] == "/":
                parameter_count -= 2
                del split_parameters[3]
            else:
                return False
        elif parameter_count >= 6:
            return False

        is_percent = split_parameters[0][-1] == "%"  # check if types are synced
        if not all(is_percent == (parameter[-1] == "%") for parameter in split_parameters[:parameter_count]):
            return False

        try:
            tuple(map(Color.__rgb_color_value_to_eight_bit, split_parameters))  # cast to tuple to execute the generator
            return True
        except ValueError:
            return False

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
        if len(split_parameters) == 5 and split_parameters[3] == "/":
            del split_parameters[3]
        int_parameters = map(Color.__rgb_color_value_to_eight_bit, split_parameters)
        hex_parameters = map(lambda p: hex(p)[2:].upper().zfill(2), int_parameters)

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

        if self.color_type not in EXPANDERS:
            raise NotImplementedError("Notation expansion cannot be performed on {}".format(self.color_type))
        if not self.is_valid:
            raise ValueError("Notation expansion cannot occur on invalid colors")

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

        if self.color_type not in ALPHA_REMOVERS:
            raise NotImplementedError("Alpha removal cannot be performed on {}".format(self.color_type))
        if not self.is_valid:
            raise ValueError("{} is not a valid color".format(self.stored_color))

        return ALPHA_REMOVERS[self.color_type](self)

    def __hex_without_alpha(self) -> Color:
        """Removes the transparency from a hex-color format color. Should be called from without_alpha.
        This function keeps the output format the same length as the input format.

        :return: A new color based on the calling color, without alpha.
        """
        color = self.stored_color
        if len(color) == 4:
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
        return color_a.stored_color.lower() == color_b.stored_color.lower()

    @staticmethod
    def get_unique_color(color_iterable: typing.Iterable[typing.Union[str | Color]]) -> Color:
        """Given an Iterable consisting of strs and or Colors, this function will return a new Color instance
        containing a unique color from the named color list, if there are unique colors remaining in the named-color
        table. If not, it returns a transparent color.

        :param color_iterable: An iterable object consisting of strings or colors.
        :return: A new Color Object as type named-color or transparent.
        """
        colors = Color.__COLOR_TO_NAME_TABLE.copy()

        for color in color_iterable:
            if isinstance(color, str):
                color = Color(color)
            if not color.is_valid:
                continue
            color = color.to_hex_color().without_alpha()
            if str(color) in colors:
                del colors[str(color)]

        if len(colors) == 0:
            return Color("transparent")
        else:
            return Color([*colors.values()][0])

    @staticmethod
    def __legacy_parameters_to_modern(legacy_params: str) -> str:
        """Converts a CSS legacy style function call to the syntax of a modern css call.

        :param legacy_params: A string containing the inner parameters of a CSS function, ex: "33, 33, 33"
        :return: A string in the modern css function call, ex: "33 33 33"
        :raise ValueError: The provided syntax is invalid, ex: 33,,,33,33
        """
        parameters = [parameter for parameter in legacy_params.replace(" ", "").split(",")]
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
