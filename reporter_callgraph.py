from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

import unittest_demo1 as demo
import HTMLTestReportEN as HTMLTestRunner
import unittest

graphviz = GraphvizOutput(output_file='reporter_graph.png')

with PyCallGraph(output=graphviz):
    reporter = "./reporter.html"

    # ok, reporter.html has data.
    tu = unittest.TestSuite()
    tu.addTest(unittest.makeSuite(demo.MathFunctionsTestCase))
    tu.addTest(unittest.makeSuite(demo.V2exAPITestCase))
    tu.addTest(unittest.makeSuite(demo.WidgetTestCase))

    # not ok, reporter has 0 data, no test case really runs.
    # tu = unittest.TestSuite()
    # tu.addTest(demo.MyTestSuit())

    # tu = unittest.TestSuite()
    # error, TypeError("TestCases and TestSuites must be instantiated "
    # tu.addTest(demo.WidgetTestCase)
    # tu.addTest(demo.V2exAPITestCase)

    fp = open(reporter, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(fp, title='unittest_demo1 reporter', description=u'This is a report test',
                                           tester="xiongyang3 from xxx dep")
    runner.run(tu)
    fp.close()

