import logging
import unittest

from nion.utils import Color


# Define static color lists for simplicity
HEX_COLORS = ['#F0F8FF', '#fFf', '#000f', '#00000000']
INVALID_HEX_COLORS = ["#banana", "#A", "#FF", "#12345", "#1234567", "#123456789"]

TRANSPARENT_COLORS = ["transparent", "TRANSPARENT", "tRaNsPaReNt"]

NAMED_COLORS = [*Color.Color._Color__NAME_TO_COLOR_TABLE.keys()]

MODERN_RGB_COLORS = ["(240 248 255)", "(255 255 255)", "(0 0 0)", "(0 0 0 0)",  # ints
                     "(240.0 247.6 255.0)", "(255.0 +255.0 255.0)", "(0.0 0.0 0.0)", "(0.0 0.0 0.0 0.0)",  # floats
                     "(2.4e2 .248e3 255e0)", "(255000e-3 2.55e2 25.5e1)", "(0.0e0 0 0.0)", "(0 0.0 -0e0 +0e-0)",  # scientific notation
                     "(94.11764705882352% 97.25490196078431% 100.0%)", "(100.0% 100.0% 100.0%)", "(0.0% 0.0% 0.0%)", "(0.0% 0.0% 0.0% 0.0%)",  # percents
                     "(240 248 255 / 255)", "(255 240.005 255 / 100%)", "(0% 0% 0% / 2.25e2)", "(0% 0% 0% / 0%)"]  # mixed
INVALID_MODERN_RGB_COLORS = ["(0 / 0 0 0)", "()", "((0 0 0 0))", "(0%, 0%, 0%, 255)", "(0, 0, 0, 100%)", "(0 255 2.25Q7, 35%%, i)", "(255.0, +255.0 255.0)"]


LEGACY_RGB_COLORS = ["(240, 248, 255)", "(255, 255, 255)", "(0, 0, 0)", "(0, 0, 0, 0)",  # ints
                     "(240.0, 247.6, 255.0)", "(255.0, +255.0, 255.0)", "(0.0, 0.0, 0.0)", "(0.0, 0.0, 0.0, 0.0)",  # floats
                     "(2.4e2, .248e3, 255e0)", "(255000e-3, 2.55e2, 25.5e1)", "(0.0e0, 0, 0.0)", "(0, 0.0, -0e0, +0e-0)",  # scientific notation
                     "(94.11764705882352%, 97.25490196078431%, 100.0%)", "(100.0%, 100.0%, 100.0%)", "(0.0%, 0.0%, 0.0%)", "(0.0%, 0.0%, 0.0%, 0.0%)"]  #percents
INVALID_LEGACY_RGB_COLORS = ["(1,,2,3), ((1,2,3,4)), (1,2,3,4,5), (1, 2, 3,,)", "(0 255 2.25Q7, 35%%, i)", "(255.0, +255.0 255.0)"]

INVALID_COLORS = ["phosphorus", "C̶̷̴H͞A҉͠O҉S̡", "overlyripebanana", "notblack", "eval(print(42))", "", "hsl(100, 25, 50"]


class TestColorClass(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_hex_color_init(self):
        for i in range(len(HEX_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color(HEX_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_named_color_init(self):
        for i in range(len(NAMED_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color(NAMED_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_transparent_init(self):
        for i in range(len(TRANSPARENT_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color(TRANSPARENT_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_rgb_init(self):
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color("rgb" + MODERN_RGB_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_legacy_rgb_init(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color("rgb" + LEGACY_RGB_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_rgba_init(self):
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color("rgba" + MODERN_RGB_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_legacy_rgba_init(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color("rgba" + LEGACY_RGB_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_unknown_init(self):
        for i in range(len(INVALID_COLORS)):
            with self.subTest(i=i):
                c = None
                try:
                    c = Color.Color("rgba" + INVALID_COLORS[i])
                except:
                    pass
                self.assertIsInstance(c, Color.Color)

    def test_stored_color(self):
        sampling = [HEX_COLORS[0], TRANSPARENT_COLORS[0], NAMED_COLORS[0], "rgb"+MODERN_RGB_COLORS[0],
                    "rgba"+MODERN_RGB_COLORS[0], "rgb"+LEGACY_RGB_COLORS[0], "rgba"+LEGACY_RGB_COLORS[0],
                    INVALID_COLORS[0], INVALID_HEX_COLORS[0], INVALID_LEGACY_RGB_COLORS[0], INVALID_MODERN_RGB_COLORS[0]]

        for i in range(len(sampling)):
            with self.subTest(i=i):
                c = Color.Color(sampling[i])
                self.assertEqual(sampling[i], c.stored_color)
                self.assertEqual(sampling[i], c._Color__stored_color)

    def test_hex_color_type(self):
        hex_colors = [*HEX_COLORS, *INVALID_HEX_COLORS]

        for i in range(len(hex_colors)):
            with self.subTest(i=i):
                c = Color.Color(hex_colors[i])
                self.assertEqual(c.color_type, "hex-color")
                self.assertEqual(c._Color__color_type, "hex-color")

    def test_named_color_type(self):
        for i in range(len(NAMED_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(NAMED_COLORS[i])
                self.assertEqual(c.color_type, "named-color")
                self.assertEqual(c._Color__color_type, "named-color")

    def test_transparent_type(self):
        for i in range(len(TRANSPARENT_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(TRANSPARENT_COLORS[i])
                self.assertEqual(c.color_type, "transparent")
                self.assertEqual(c._Color__color_type, "transparent")

    def test_rgb_type(self):
        rgb_colors = [*MODERN_RGB_COLORS, *INVALID_MODERN_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+rgb_colors[i])
                self.assertEqual(c.color_type, "rgb")
                self.assertEqual(c._Color__color_type, "rgb")

    def test_legacy_rgb_type(self):
        rgb_colors = [*LEGACY_RGB_COLORS, *INVALID_LEGACY_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgb" + rgb_colors[i])
                self.assertEqual(c.color_type, "rgb")
                self.assertEqual(c._Color__color_type, "rgb")

    def test_rgba_type(self):
        rgb_colors = [*MODERN_RGB_COLORS, *INVALID_MODERN_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + rgb_colors[i])
                self.assertEqual(c.color_type, "rgba")
                self.assertEqual(c._Color__color_type, "rgba")

    def test_legacy_rgba_type(self):
        rgb_colors = [*LEGACY_RGB_COLORS, *INVALID_LEGACY_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + rgb_colors[i])
                self.assertEqual(c.color_type, "rgba")
                self.assertEqual(c._Color__color_type, "rgba")

    def test_unknown_type(self):
        for i in range(len(INVALID_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_COLORS[i])
                self.assertEqual(c.color_type, "unknown")
                self.assertEqual(c._Color__color_type, "unknown")

    def test_hex_color_params(self):
        hex_colors = [*HEX_COLORS, *INVALID_HEX_COLORS]

        for i in range(len(hex_colors)):
            with self.subTest(i=i):
                c = Color.Color(hex_colors[i])
                self.assertEqual(c.color_parameters, "")
                self.assertEqual(c._Color__color_parameters, "")

    def test_named_color_params(self):
        for i in range(len(NAMED_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(NAMED_COLORS[i])
                self.assertEqual(c.color_parameters, "")
                self.assertEqual(c._Color__color_parameters, "")

    def test_transparent_params(self):
        for i in range(len(TRANSPARENT_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(TRANSPARENT_COLORS[i])
                self.assertEqual(c.color_parameters, "")
                self.assertEqual(c._Color__color_parameters, "")

    def test_rgb_params(self):
        rgb_colors = [*MODERN_RGB_COLORS, *INVALID_MODERN_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgb" + rgb_colors[i])
                self.assertEqual(c.color_parameters, rgb_colors[i][1:-1])
                self.assertEqual(c._Color__color_parameters, rgb_colors[i][1:-1])

    def test_legacy_rgb_params(self):
        rgb_colors = [*LEGACY_RGB_COLORS, *INVALID_LEGACY_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgb" + rgb_colors[i])
                self.assertEqual(c.color_parameters, rgb_colors[i][1:-1])
                self.assertEqual(c._Color__color_parameters, rgb_colors[i][1:-1])

    def test_rgba_params(self):
        rgb_colors = [*MODERN_RGB_COLORS, *INVALID_MODERN_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + rgb_colors[i])
                self.assertEqual(c.color_parameters, rgb_colors[i][1:-1])
                self.assertEqual(c._Color__color_parameters, rgb_colors[i][1:-1])

    def test_legacy_rgba_params(self):
        rgb_colors = [*LEGACY_RGB_COLORS, *INVALID_LEGACY_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + rgb_colors[i])
                self.assertEqual(c.color_parameters, rgb_colors[i][1:-1])
                self.assertEqual(c._Color__color_parameters, rgb_colors[i][1:-1])

    def test_unknown_params(self):
        param_key = ["", "", "", "", "print(42)", "", ""]

        for i in range(len(INVALID_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_COLORS[i])
                self.assertEqual(c.color_parameters, param_key[i])
                self.assertEqual(c._Color__color_parameters, param_key[i])

    def test_hex_color_func(self):
        hex_colors = [*HEX_COLORS, *INVALID_HEX_COLORS]

        for i in range(len(hex_colors)):
            with self.subTest(i=i):
                c = Color.Color(hex_colors[i])
                self.assertEqual(c.is_function, False)
                self.assertEqual(c._Color__is_function, False)

    def test_named_color_func(self):
        for i in range(len(NAMED_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(NAMED_COLORS[i])
                self.assertEqual(c.is_function, False)
                self.assertEqual(c._Color__is_function, False)

    def test_transparent_func(self):
        for i in range(len(TRANSPARENT_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(TRANSPARENT_COLORS[i])
                self.assertEqual(c.is_function, False)
                self.assertEqual(c._Color__is_function, False)

    def test_rgb_func(self):
        rgb_colors = [*MODERN_RGB_COLORS, *INVALID_MODERN_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgb" + rgb_colors[i])
                self.assertEqual(c.is_function, True)
                self.assertEqual(c._Color__is_function, True)

    def test_legacy_rgb_func(self):
        rgb_colors = [*LEGACY_RGB_COLORS, *INVALID_LEGACY_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgb" + rgb_colors[i])
                self.assertEqual(c.is_function, True)
                self.assertEqual(c._Color__is_function, True)

    def test_rgba_func(self):
        rgb_colors = [*MODERN_RGB_COLORS, *INVALID_MODERN_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + rgb_colors[i])
                self.assertEqual(c.is_function, True)
                self.assertEqual(c._Color__is_function, True)

    def test_legacy_rgba_func(self):
        rgb_colors = [*LEGACY_RGB_COLORS, *INVALID_LEGACY_RGB_COLORS]

        for i in range(len(rgb_colors)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + rgb_colors[i])
                self.assertEqual(c.is_function, True)
                self.assertEqual(c._Color__is_function, True)

    def test_unknown_func(self):
        func_key = [False, False, False, False, True, False, False]

        for i in range(len(INVALID_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_COLORS[i])
                self.assertEqual(c.is_function, func_key[i])
                self.assertEqual(c._Color__is_function, func_key[i])

    def test_hex_color_valid(self):
        for i in range(len(HEX_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(HEX_COLORS[i])
                self.assertEqual(c.is_valid, True)
                self.assertEqual(c._Color__is_valid, True)

        for i in range(len(INVALID_HEX_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_HEX_COLORS[i])
                self.assertEqual(c.is_valid, False)
                self.assertEqual(c._Color__is_valid, False)

    def test_named_color_valid(self):
        for i in range(len(NAMED_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(NAMED_COLORS[i])
                self.assertEqual(c.is_valid, True)
                self.assertEqual(c._Color__is_valid, True)

    def test_transparent_valid(self):
        for i in range(len(TRANSPARENT_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(TRANSPARENT_COLORS[i])
                self.assertEqual(c.is_valid, True)
                self.assertEqual(c._Color__is_valid, True)

    def test_rgb_valid(self):
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+MODERN_RGB_COLORS[i])
                self.assertEqual(c.is_valid, True)
                self.assertEqual(c._Color__is_valid, True)

        for i in range(len(INVALID_MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+INVALID_MODERN_RGB_COLORS[i])
                self.assertEqual(c.is_valid, False)
                self.assertEqual(c._Color__is_valid, False)

    def test_legacy_rgb_valid(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+LEGACY_RGB_COLORS[i])
                self.assertEqual(c.is_valid, True)
                self.assertEqual(c._Color__is_valid, True)

        for i in range(len(INVALID_LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+INVALID_LEGACY_RGB_COLORS[i])
                self.assertEqual(c.is_valid, False)
                self.assertEqual(c._Color__is_valid, False)

    def test_rgba_valid(self):
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba"+MODERN_RGB_COLORS[i])
                self.assertEqual(c.is_valid, True)
                self.assertEqual(c._Color__is_valid, True)

        for i in range(len(INVALID_MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba"+INVALID_MODERN_RGB_COLORS[i])
                self.assertEqual(c.is_valid, False)
                self.assertEqual(c._Color__is_valid, False)

    def test_legacy_rgba_valid(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba"+LEGACY_RGB_COLORS[i])
                self.assertEqual(c.is_valid, True)
                self.assertEqual(c._Color__is_valid, True)

        for i in range(len(INVALID_LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba"+INVALID_LEGACY_RGB_COLORS[i])
                self.assertEqual(c.is_valid, False)
                self.assertEqual(c._Color__is_valid, False)

    def test_unknown_valid(self):
        for i in range(len(INVALID_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_COLORS[i])
                self.assertEqual(c.is_valid, False)
                self.assertEqual(c._Color__is_valid, False)

    def test_hex_color_to_hex(self):
        ...

    def test_named_color_to_hex(self):
        ...

    def test_transparent_to_hex(self):
        ...

    def test_rgb_to_hex(self):
        ...

    def test_legacy_rgb_to_hex(self):
        ...

    def test_rgba_to_hex(self):
        ...

    def test_legacy_rgba_to_hex(self):
        ...

    def test_unknown_to_hex(self):
        ...

    def test_hex_color_expand(self):
        ...

    def test_named_color_expand(self):
        ...

    def test_transparent_expand(self):
        ...

    def test_rgb_expand(self):
        ...

    def test_legacy_rgb_expand(self):
        ...

    def test_rgba_expand(self):
        ...

    def test_legacy_rgba_expand(self):
        ...

    def test_unknown_expand(self):
        ...

    def test_hex_color_alpha(self):
        ...

    def test_named_color_alpha(self):
        ...

    def test_transparent_alpha(self):
        ...

    def test_rgb_alpha(self):
        ...

    def test_legacy_rgb_alpha(self):
        ...

    def test_rgba_alpha(self):
        ...

    def test_legacy_rgba_alpha(self):
        ...

    def test_unknown_alpha(self):
        ...

    def test_equality(self):
        ...

    def test_str(self):
        ...

    def test_repr(self):
        ...