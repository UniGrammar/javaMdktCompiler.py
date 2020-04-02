#!/usr/bin/env python3
import sys
import unittest
from collections import OrderedDict
from pathlib import Path

thisDir = Path(__file__).absolute().parent
parentDir = thisDir.parent

sys.path.insert(0, str(parentDir))

dict = OrderedDict

from javaMdktCompiler import javaCompile, mdktNS

compilerSources = list((parentDir / mdktNS / "src" / "main" / "java" / "/".join(mdktNS.split("."))).glob("*.java"))


class Tests(unittest.TestCase):
	def testCompileTest(self):
		res = javaCompile([thisDir / "Test.java"])
		t = res["Test"]()
		tr = str(t.test())
		self.assertEqual(tr, "test")

	@unittest.skip
	def testCompile(self):
		res = javaCompile(compilerSources)
		print(res)


if __name__ == "__main__":
	unittest.main()
