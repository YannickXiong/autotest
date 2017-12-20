import unittest
import requests
import HTMLTestRunner

"""
使用unittest的话需要记住下面的几点
  - 导入unittest
  - 定义继承自unittest.TestCase的测试类，类名可以随便取
  - 定义以test开头的测试方法，这个方法就是测试用例，你可以在一个类里定义n个测试用例
  - 断言，用来判断结果
  - unittest.main()是执行测试用例最简单的方式
  - 有点恶心的一点，无法在pycharm里直接运行UT的用例，只能在终端使用python xxx来运行，这个问题可以参考
    http://www.cnblogs.com/csjd/p/6366535.html

运行命令：
    python3 -m unittest -v unittest_demo1.py 
"""


# style 1: testCase for API
class V2exAPITestCase(unittest.TestCase):

    # init the data
    def setUp(self):
        self.url = "https://www.v2ex.com/api/nodes/show.json"

    def test_v2ex_api_normal(self):
        # 3A: Arrange
        querystring = {"name": "python"}

        # 3A: Action
        self.assertIsNotNone(self.url)
        response = requests.request("GET", self.url, params=querystring).json()

        # 3A: Assert
        self.assertEqual(response['name'], 'python')
        self.assertEqual(response['id'], 90)

    def test_v2ex_api_no_object(self):
        # 3A: Arrange
        querystring = {"name": ""}

        # 3A: Action
        self.assertIsNotNone(self.url)
        response = requests.request("GET", self.url, params=querystring).json()

        # 3A: Assert
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['message'], 'Object Not Found')

    # destroy the data
    def tearDown(self):
        self.url = None


# the class need to be tested.
class Widget:
    def __init__(self, size=(40, 40)):
        self._size = size

    def get_size(self):
        return self._size

    def resize(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("Illegal size")
        self._size = (width, height)

    def dispose(self):
        pass


# style 2: testCase for a class
class WidgetTestCase(unittest.TestCase):
    # init the data
    def setUp(self):
        self.widget = Widget()
        self.default_size = (40, 40)
        self.exception_size = [(-40, 40), (0, -40), (-40, -40)]
        self.normal_size = [(0, 40), (40, 0), (0, 0), (40, 40)]

    def test_widget_default_size(self):
        self.assertEqual(self.widget.get_size(), self.default_size)

    def test_widget_reset_size_exception(self):
        for _size in self.exception_size:
            # assertRaises(expected exception, function, arguments of function)
            # attention: assertRaises need the function name, not function called. So self.widget.resize() will raise
            # exception.
            self.assertRaises(ValueError, self.widget.resize, _size[0], _size[1])

    def test_weight_reset_size_normal(self):
        for _size in self.normal_size:
            self.widget.resize(_size[0], _size[1])
            self.assertEqual(self.widget.get_size(), _size)

    # destroy the data
    def tearDown(self):
        self.widget = None
        self.default_size = None
        self.exception_size = None
        self.normal_size = None


# the functions need to be tested
def add(a, b):
    return a + b


def minus(a, b):
    return a - b


def multi(a, b):
    return a * b


def divide(a, b):
    if not b or b == 0:
        raise ValueError("Invalid dividend, the dividend can not be None or 0.")
    return a / b


# style3: testCase for functions
class MathFunctionsTestCase(unittest.TestCase):
    # init the data
    def setUp(self):
        self.num_list = [(-12.3, 5), (0, 10), (300, 12), (5, 2), (-2, -45)]
        self.exception_num_list = [(0, 0)]

    def test_add(self):
        for _number in self.num_list:
            self.assertEqual(add(_number[0], _number[1]), sum(_number))

    def test_minus(self):
        for _number in self.num_list:
            self.assertEqual(minus(_number[0], _number[1]), _number[0] - _number[1])

    def test_multi(self):
        for _number in self.num_list:
            self.assertEqual(multi(_number[0], _number[1]), _number[0] * _number[1])

    def test_divide(self):
        for _number in self.num_list:
            self.assertEqual(divide(_number[0], _number[1]), _number[0] / _number[1])

    def test_divide_exception(self):
        for _number in self.exception_num_list:
            self.assertRaises(ValueError, divide, _number[0], _number[1])

    def tearDown(self):
        self.num_list = None
        self.exception_num_list = None


# test suit
class MyTestSuit(unittest.TestSuite):
    def get_suit(self):
        self.addTest(V2exAPITestCase())
        # add more test cases.
        self.addTest(WidgetTestCase())
        # I found that the execute order of the testCases in a testSuit is based on the testCase name.
        # if test cases are: V2exAPITestCase(), WidgetTestCase(), MathFunctionsTestCase, the order is.
        #   - run MathFunctionsTestCase
        #   - run V2exAPITestCase()
        #   - run WidgetTestCase()
        # if test cases are: V2exAPITestCase(), WidgetTestCase(), ZMathFunctionsTestCase, the order is.
        #   - run V2exAPITestCase()
        #   - run WidgetTestCase()
        # - run ZMathFunctionsTestCase
        self.addTest(MathFunctionsTestCase())
        return self


if __name__ == '__main__':
    unittest.main(defaultTest=MyTestSuit())
