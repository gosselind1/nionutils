import logging
import unittest

from nion.utils import Color


# Define static color lists for simplicity
HEX_COLORS = ['#F0F8FF', '#fFf', '#000f', '#00000000']
INVALID_HEX_COLORS = ["#banana", "#A", "#FF", "#12345", "#1234567", "#123456789"]

TRANSPARENT_COLORS = ["transparent", "TRANSPARENT", "tRaNsPaReNt"]

NAMED_COLORS = [*Color.Color._Color__NAME_TO_COLOR_TABLE.keys()]

MODERN_RGB_COLORS = ["(240  248 255)", "(255 255 255)", "(0 0 0)", "(0 0 0 0)",  # ints
                     "(240.0 247.6 255.0)", "(255.0 +255.0 255.0)", "(0.0 0.0 0.0)", "(0.0 0.0 0.0 0.0)",  # floats
                     "(2.4e2 .248e3 255e0)", "(255000e-3 2.55e2 25.5e1)", "(0.0e0 0 0.0)", "(0 0.0 -0e0 +0e-0)",  # scientific notation
                     "(94.11764705882352% 97.25490196078431%   100.0%)", "(100.0% 100.0% 100.0%)", "(0.0% 0.0% 0.0%)", "(0.0% 0.0% 0.0% 0.0%)",  # percents
                     "(240 248 255 / 255)", "(255 240.005 255 / 100%)", "(0% 0% 0% / 2.25e2)", "(0% 0% 0% / 0%)"]  # mixed
INVALID_MODERN_RGB_COLORS = ["(0 / 0 0 0)", "()", "((0 0 0 0))", "(0%, 0%, 0%, 255)", "(0, 0, 0, 100%)", "(0 255 2.25Q7, 35%%, i)", "(255.0, +255.0 255.0)"]


LEGACY_RGB_COLORS = ["(240,  248, 255)", "(255, 255, 255)", "(0, 0, 0)", "(0, 0, 0, 0)",  # ints
                     "(240.0, 247.6, 255.0)", "(255.0, +255.0, 255.0)", "(0.0, 0.0, 0.0)", "(0.0, 0.0, 0.0, 0.0)",  # floats
                     "(2.4e2, .248e3, 255e0)", "(255000e-3, 2.55e2, 25.5e1)", "(0.0e0, 0, 0.0)", "(0, 0.0, -0e0, +0e-0)",  # scientific notation
                     "(94.11764705882352%, 97.25490196078431%,   100.0%)", "(100.0%, 100.0%, 100.0%)", "(0.0%, 0.0%, 0.0%)", "(0.0%, 0.0%, 0.0%, 0.0%)"]  #percents
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

    def test_str(self):
        sampling = [HEX_COLORS[0], TRANSPARENT_COLORS[0], NAMED_COLORS[0], "rgb" + MODERN_RGB_COLORS[0],
                    "rgba" + MODERN_RGB_COLORS[0], "rgb" + LEGACY_RGB_COLORS[0], "rgba" + LEGACY_RGB_COLORS[0],
                    INVALID_COLORS[0], INVALID_HEX_COLORS[0], INVALID_LEGACY_RGB_COLORS[0],
                    INVALID_MODERN_RGB_COLORS[0]]

        for i in range(len(sampling)):
            with self.subTest(i=i):
                c = Color.Color(sampling[i])
                self.assertEqual(str(c), sampling[i])

    def test_repr(self):
        sampling = [HEX_COLORS[0], TRANSPARENT_COLORS[0], NAMED_COLORS[0], "rgb" + MODERN_RGB_COLORS[0],
                    "rgba" + MODERN_RGB_COLORS[0], "rgb" + LEGACY_RGB_COLORS[0], "rgba" + LEGACY_RGB_COLORS[0],
                    INVALID_COLORS[0], INVALID_HEX_COLORS[0], INVALID_LEGACY_RGB_COLORS[0],
                    INVALID_MODERN_RGB_COLORS[0]]

        for i in range(len(sampling)):
            with self.subTest(i=i):
                c = Color.Color(sampling[i])
                self.assertEqual(repr(c), repr(sampling[i]))

    def test_hex_color_to_hex(self):
        hex_colors = [*HEX_COLORS, *INVALID_HEX_COLORS]

        for i in range(len(hex_colors)):
            with self.subTest(i=i):
                c = Color.Color(hex_colors[i])
                self.assertEqual(c.stored_color, c.to_hex_color().stored_color)

    def test_named_color_to_hex(self):
        for i in range(len(NAMED_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(NAMED_COLORS[i])
                as_hex = str(c.to_hex_color())

                # We have to do these checks / replacements because multiple names map to a single hex value.
                # Therefore, depending on how things are initialized, there might be some valid alternative names
                color_name = Color.Color._Color__COLOR_TO_NAME_TABLE[as_hex]
                color_name = color_name.replace("grey", "gray")

                target_name = NAMED_COLORS[i]
                target_name = target_name.replace("grey", "gray")

                if color_name != target_name:
                    if target_name == "cyan":
                        target_name = "aqua"
                    elif target_name == "aqua":
                        target_name = "cyan"
                    elif target_name == "magenta":
                        target_name = "fuchsia"
                    elif target_name == "fuchsia":
                        target_name = "magenta"

                self.assertEqual(color_name, target_name)

    def test_transparent_to_hex(self):
        for i in range(len(TRANSPARENT_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(TRANSPARENT_COLORS[i])
                self.assertEqual(str(c.to_hex_color()), "#00000000")

    def test_rgb_to_hex(self):
        # since all colors are guaranteed to be of a sub-spec, we can be a bit crude in getting a conversion
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb" + MODERN_RGB_COLORS[i])
                h = MODERN_RGB_COLORS[i][1:-1]
                h = [b for b in h.split(" ") if len(b)]
                if len(h) == 5:
                    del h[3]

                for b in range(len(h)):
                    if h[b][-1] == "%":
                        h[b] = h[b][:-1]
                        h[b] = round(float(h[b]) * 255)
                    else:
                        h[b] = round(float(h[b]))

                    h[b] = min(h[b], 255)
                    h[b] = max(h[b], 0)
                    h[b] = hex(h[b])[2:].upper().zfill(2)

                h = "#" + "".join(h)

                self.assertEqual(str(c.to_hex_color()), h)

        for i in range(len(INVALID_MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_MODERN_RGB_COLORS[i])
                error = False
                try:
                    c.to_hex_color()
                except NotImplementedError:
                    error = True
                self.assertEqual(error, True)

    def test_legacy_rgb_to_hex(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb" + LEGACY_RGB_COLORS[i])
                h = LEGACY_RGB_COLORS[i][1:-1]
                h.replace(" ", "")
                h = [b for b in h.split(",") if len(b)]

                for b in range(len(h)):
                    if h[b][-1] == "%":
                        h[b] = h[b][:-1]
                        h[b] = round(float(h[b]) * 255)
                    else:
                        h[b] = round(float(h[b]))

                    h[b] = min(h[b], 255)
                    h[b] = max(h[b], 0)
                    h[b] = hex(h[b])[2:].upper().zfill(2)

                h = "#" + "".join(h)

                self.assertEqual(str(c.to_hex_color()), h)

        for i in range(len(INVALID_LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_LEGACY_RGB_COLORS[i])
                error = False
                try:
                    c.to_hex_color()
                except NotImplementedError:
                    error = True
                self.assertEqual(error, True)

    def test_rgba_to_hex(self):
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + MODERN_RGB_COLORS[i])
                h = MODERN_RGB_COLORS[i][1:-1]
                h = [b for b in h.split(" ") if len(b)]
                if len(h) == 5:
                    del h[3]

                for b in range(len(h)):
                    if h[b][-1] == "%":
                        h[b] = h[b][:-1]
                        h[b] = round(float(h[b]) * 255)
                    else:
                        h[b] = round(float(h[b]))

                    h[b] = min(h[b], 255)
                    h[b] = max(h[b], 0)
                    h[b] = hex(h[b])[2:].upper().zfill(2)

                h = "#" + "".join(h)

                self.assertEqual(str(c.to_hex_color()), h)

        for i in range(len(INVALID_MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_MODERN_RGB_COLORS[i])
                error = False
                try:
                    c.to_hex_color()
                except NotImplementedError:
                    error = True
                self.assertEqual(error, True)

    def test_legacy_rgba_to_hex(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + LEGACY_RGB_COLORS[i])
                h = LEGACY_RGB_COLORS[i][1:-1]
                h.replace(" ", "")
                h = [b for b in h.split(",") if len(b)]

                for b in range(len(h)):
                    if h[b][-1] == "%":
                        h[b] = h[b][:-1]
                        h[b] = round(float(h[b]) * 255)
                    else:
                        h[b] = round(float(h[b]))

                    h[b] = min(h[b], 255)
                    h[b] = max(h[b], 0)
                    h[b] = hex(h[b])[2:].upper().zfill(2)

                h = "#" + "".join(h)

                self.assertEqual(str(c.to_hex_color()), h)

        for i in range(len(INVALID_LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_LEGACY_RGB_COLORS[i])
                error = False
                try:
                    c.to_hex_color()
                except NotImplementedError:
                    error = True
                self.assertEqual(error, True)

    def test_unknown_to_hex(self):
        for i in range(len(INVALID_COLORS)):
            with self.subTest(i=i):
                error = False
                c = Color.Color(INVALID_COLORS[i])
                try:
                    c.to_hex_color()
                except NotImplementedError:
                    error = True
                finally:
                    self.assertEqual(error, True)

    def test_hex_color_expand(self):
        for i in range(len(HEX_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(HEX_COLORS[i])
                c = c.to_expanded_notation()
                e = HEX_COLORS[i][1:]
                if len(e) == 3:
                    e = e + "F"
                if len(e) == 4:
                    e = "".join(c*2 for c in e)
                if len(e) == 6:
                    e = e + "FF"
                self.assertEqual(str(c), "#"+e)

        for i in range(len(INVALID_HEX_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_HEX_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except ValueError:
                    error = True
                self.assertEqual(error, True)

    def test_named_color_expand(self):
        for i in range(len(NAMED_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(NAMED_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except NotImplementedError:
                    error = True
                self.assertEqual(error, True)

    def test_transparent_expand(self):
        for i in range(len(TRANSPARENT_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(TRANSPARENT_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except NotImplementedError:
                    error = True
                self.assertEqual(error, True)

    def test_rgb_expand(self):
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+MODERN_RGB_COLORS[i])
                c = c.to_expanded_notation()

                e = [v for v in MODERN_RGB_COLORS[i][1:-1].split(" ") if len(v)]
                if len(e) == 3:
                    e.append("/")
                    e.append("255")
                if len(e) == 4:
                    e.insert(3, "/")
                e = "rgb(" + " ".join(e) + ")"
                self.assertEqual(str(c), e)

        for i in range(len(INVALID_MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+INVALID_MODERN_RGB_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except ValueError:
                    error = True
                self.assertEqual(error, True)

    def test_legacy_rgb_expand(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+LEGACY_RGB_COLORS[i])
                c = c.to_expanded_notation()

                e = LEGACY_RGB_COLORS[i][1:-1].replace(" ", "")
                e = [v for v in e.split(",") if len(v)]
                if len(e) == 3:
                    e.append("255")
                e = "rgb(" + ", ".join(e) + ")"
                self.assertEqual(str(c), e)

        for i in range(len(INVALID_LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgb"+INVALID_LEGACY_RGB_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except ValueError:
                    error = True
                self.assertEqual(error, True)

    def test_rgba_expand(self):
        for i in range(len(MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + MODERN_RGB_COLORS[i])
                c = c.to_expanded_notation()

                e = [v for v in MODERN_RGB_COLORS[i][1:-1].split(" ") if len(v)]
                if len(e) == 3:
                    e.append("/")
                    e.append("255")
                if len(e) == 4:
                    e.insert(3, "/")
                e = "rgba(" + " ".join(e) + ")"
                self.assertEqual(str(c), e)

        for i in range(len(INVALID_MODERN_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba" + INVALID_MODERN_RGB_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except ValueError:
                    error = True
                self.assertEqual(error, True)

    def test_legacy_rgba_expand(self):
        for i in range(len(LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba"+LEGACY_RGB_COLORS[i])
                c = c.to_expanded_notation()

                e = LEGACY_RGB_COLORS[i][1:-1].replace(" ", "")
                e = [v for v in e.split(",") if len(v)]
                if len(e) == 3:
                    e.append("255")
                e = "rgba(" + ", ".join(e) + ")"
                self.assertEqual(str(c), e)

        for i in range(len(INVALID_LEGACY_RGB_COLORS)):
            with self.subTest(i=i):
                c = Color.Color("rgba"+INVALID_LEGACY_RGB_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except ValueError:
                    error = True
                self.assertEqual(error, True)

    def test_unknown_expand(self):
        for i in range(len(INVALID_COLORS)):
            with self.subTest(i=i):
                c = Color.Color(INVALID_COLORS[i])
                error = False
                try:
                    c.to_expanded_notation()
                except NotImplementedError:
                    error = True
                self.assertEqual(error, True)

    def test_equality(self):
        a_colors = ["#000000", "#FfF", "rgba(0, 255, 0)", "cyan", "transparent"]
        b_colors = ["rgb(0 0 0 / 0)", "white", "rgb(0 255 0 / 100%)", "aqua", "#00000000"]
        equal = [False, True, True, True, True]

        for i in range(len(a_colors)):
            with self.subTest(i=i):
                a_c = Color.Color(a_colors[i])
                b_c = Color.Color(b_colors[i])
                self.assertEqual(a_c == b_c, equal[i])

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
