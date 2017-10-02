# -*- coding: utf-8 -*-



import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath

#from OPL_Testing.TC_T014474 import TC_T014474

from OPL_Testing.TC_T016944 import TC_T016944

if __name__ == '__main__':

    '''
    suite_template = unittest.TestSuite()
    suite_template.addTest(TestCase_1("test_number1"))
    suite_template.addTest(TestCase_1("test_number2"))

    suiteLive = unittest.TestLoader().loadTestsFromTestCase(TestLiveBasics)

    alltests = unittest.TestSuite([suite_template, suiteLive])

    runner = XMLTestRunner(Env.XML_DIR)
    runner.run(alltests)


    suiteLive = unittest.TestSuite()

    suiteLive.addTest(TestLiveBasics("test_1_zapping"))

    '''
    suiteLive = unittest.TestLoader().loadTestsFromTestCase(TC_T016944)


    runner = XMLTestRunner(createAndGetXmlDirPath())
    runner.run(suiteLive)