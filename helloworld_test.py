#!/usr/bin/python
import unittest
import helloworld

class HelloWorldTest(unittest.TestCase):
  def testPrintSum(self):
    self.assertEquals(8, helloworld.printSum(3,5), "Checking Sum method")

  def testPrintSum1(self):
    self.assertEquals(9, helloworld.printSum(3,6), "Checking Sum method")

if __name__ == '__main__':
  unittest.main()
