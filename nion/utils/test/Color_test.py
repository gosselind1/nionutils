# standard libraries
import logging
import unittest

from nion.utils import Color


class TestColorClass(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_valid_named_inputs(self):
        colors = ['aliceblue', 'white', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'transparent']
        rgba_tuples = [[240, 248, 255], [255, 255, 255], [0, 255, 255], [127, 255, 212], [240, 255, 255],
                       [245, 245, 220], [255, 228, 196], [0, 0, 0], [0, 0, 0, 0]]

        self.__test_colors(rgba_tuples, colors)

    def test_valid_hex_inputs(self):
        colors = ['#F0F8FF', '#fFf', '#000f', '#00000000']
        rgba_tuples = [[240, 248, 255], [255, 255, 255], [0, 0, 0, 255], [0, 0, 0, 0]]

        self.__test_colors(rgba_tuples, colors)

    def test_valid_legacy_rgb_inputs(self):
        rgba_tuples = [[240, 248, 255], [255, 255, 255], [0, 0, 0], [0, 0, 0, 0]]

        int_colors = ["(240, 248, 255)", "(255, 255, 255)", "(0, 0, 0)", "(0, 0, 0, 0)"]
        self.__test_colors(rgba_tuples, ["rgb"+c for c in int_colors])
        self.__test_colors(rgba_tuples, ["rgba"+c for c in int_colors])

        float_colors = ["(240.0, 247.6, 255.0)", "(255.0, +255.0, 255.0)", "(0.0, 0.0, 0.0)", "(0.0, 0.0, 0.0, 0.0)"]
        self.__test_colors(rgba_tuples, ["rgb"+c for c in float_colors])
        self.__test_colors(rgba_tuples, ["rgba"+c for c in float_colors])

        scientific_colors = ["(2.4e2, .248e3, 255e0)", "(255000e-3, 2.55e2, 25.5e1)", "(0.0e0, 0, 0.0)", "(0, 0.0, -0e0, +0e-0)"]
        self.__test_colors(rgba_tuples, ["rgb"+c for c in scientific_colors])
        self.__test_colors(rgba_tuples, ["rgba"+c for c in scientific_colors])

        percent_colors = [str(tuple(str(component / 255)+"%" for component in color)) for color in rgba_tuples]
        self.__test_colors(rgba_tuples, ["rgb"+c for c in percent_colors])
        self.__test_colors(rgba_tuples, ["rgba"+c for c in percent_colors])

    def test_valid_modern_rgb_inputs(self):
        rgba_tuples = [[240, 248, 255], [255, 255, 255], [0, 0, 0], [0, 0, 0, 0]]

        int_colors = ["(240 248 255)", "(255 255 255)", "(0 0 0)", "(0 0 0 0)"]
        self.__test_colors(rgba_tuples, ["rgb" + c for c in int_colors])
        self.__test_colors(rgba_tuples, ["rgba" + c for c in int_colors])

        float_colors = ["(240.0 247.6 255.0)", "(255.0 +255.0 255.0)", "(0.0 0.0 0.0)", "(0.0 0.0 0.0 0.0)"]
        self.__test_colors(rgba_tuples, ["rgb" + c for c in float_colors])
        self.__test_colors(rgba_tuples, ["rgba" + c for c in float_colors])

        scientific_colors = ["(2.4e2 .248e3 255e0)", "(255000e-3 2.55e2 25.5e1)", "(0.0e0 0 0.0)", "(0 0.0 -0e0 +0e-0)"]
        self.__test_colors(rgba_tuples, ["rgb" + c for c in scientific_colors])
        self.__test_colors(rgba_tuples, ["rgba" + c for c in scientific_colors])

        percent_colors = [str(tuple(str(component / 255).replace(",", "") + "%" for component in color)) for color in rgba_tuples]
        self.__test_colors(rgba_tuples, ["rgb" + c for c in percent_colors])
        self.__test_colors(rgba_tuples, ["rgba" + c for c in percent_colors])

        mixed_colors = ["(240 248 255 / 255)", "(255 255 255 / 100%)", "(0% 0% 0% / 255)", "(0% 0% 0% / 0%)"]
        self.__test_colors(rgba_tuples, ["rgb" + c for c in mixed_colors])
        self.__test_colors(rgba_tuples, ["rgba" + c for c in mixed_colors])

    def test_invalid_named_inputs(self):
        colors = ["C̶̷̴H͞A҉͠O҉S̡", "overlyripebanana", "notblack", "eval(print(42))", ""]
        rgba_tuples = [[0, 0, 0, 255]] * len(colors)

        self.__test_colors(rgba_tuples, colors)

    def test_invalid_hex_inputs(self):
        colors = ["#banana", "#A", "#FF", "#12345", "#1234567", "#123456789"]
        rgba_tuples = [[0, 0, 0, 255]] * len(colors)

        self.__test_colors(rgba_tuples, colors)

    def test_invalid_legacy_rgb_inputs(self):
        colors = ["(1,,2,3), ((1,2,3,4)), (1,2,3,4,5), (1, 2, 3,,)"]
        rgba_tuples = [[0, 0, 0, 255]] * len(colors)

        self.__test_colors(rgba_tuples, ["rgb" + c for c in colors])
        self.__test_colors(rgba_tuples, ["rgba" + c for c in colors])

    def test_invalid_modern_rgb_inputs(self):
        colors = ["(0 / 0 0 0)", "()", "((0 0 0 0))", "(0%, 0%, 0%, 255)", "(0, 0, 0, 100%)"]
        rgba_tuples = [[0, 0, 0, 255]] * len(colors)

        self.__test_colors(rgba_tuples, colors)

    def test_other_invalid_inputs(self):
        colors = []
        rgba_tuples = [[0, 0, 0, 255]] * len(colors)

        self.__test_colors(rgba_tuples, colors)

    def __test_colors(self, rgba_tuples, colors):
        assert len(colors) == len(rgba_tuples)
        message = "Expected {} value of {} for {}"

        for i in range(len(colors)):
            with self.subTest(i=i):
                c = Color.Color(colors[i])
                self.assertEqual(c.r, rgba_tuples[i][0], message.format("r", rgba_tuples[0], colors[i]))
                self.assertEqual(c.r, rgba_tuples[i][0], message.format("g", rgba_tuples[1], colors[i]))
                self.assertEqual(c.r, rgba_tuples[i][0], message.format("b", rgba_tuples[2], colors[i]))
                if len(rgba_tuples[i]) != 4:
                    alpha = 255
                else:
                    alpha = rgba_tuples[i][3]
                self.assertEqual(c.r, rgba_tuples[i][0], message.format("a", alpha, colors[i]))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
