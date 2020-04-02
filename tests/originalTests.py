#!/usr/bin/env python3
import sys
import unittest
from collections import OrderedDict
from pathlib import Path

dict = OrderedDict

thisDir = Path(__file__).absolute().parent
parentDir = thisDir.parent

sys.path.insert(0, str(parentDir))

from javaMdktCompiler import javaCompile, mdktNS, CompilationException, ji

testsSourcesDir = parentDir / mdktNS / "src" / "test" / "resources"

__license__ = "Apache-2.0"
__copyright__ = "Copyright 2015 trung"


class OriginalTests(unittest.TestCase):
	"""
	Original tests ported from Java to Python 3
	See org.mdkt.compiler/src/test/java/org/mdkt/compiler/InMemoryJavaCompilerTest.java For the original
	"""

	def getResourceAsString(self, subpath):
		return (testsSourcesDir / subpath).read_text()

	def test_compile_WhenTypical(self):
		helloClass = javaCompile([("org.mdkt.HelloClass", self.getResourceAsString("compile_WhenTypical/HelloClass.java"))])["org.mdkt.HelloClass"]
		self.assertIsNotNone(helloClass)
		self.assertEqual(1, int(ji.reflectClass(helloClass).getDeclaredMethods().length))

	def test_compileAll_WhenTypical(self):
		compiled = javaCompile([
			("A", self.getResourceAsString("compileAll_WhenTypical/A.java")),
			("B", self.getResourceAsString("compileAll_WhenTypical/B.java"))
		])

		self.assertIsNotNone(compiled.get("A"))
		self.assertIsNotNone(compiled.get("B"))

		aClass = compiled.get("A")
		a = aClass()
		self.assertEqual("B!", str(a.b().toString()))

	def test_compile_WhenSourceContainsInnerClasses(self):
		helloClass = javaCompile([("org.mdkt.HelloClass", self.getResourceAsString("compile_WhenSourceContainsInnerClasses/HelloClass.java"))])["org.mdkt.HelloClass"]
		self.assertIsNotNone(helloClass)
		self.assertEqual(1, int(ji.reflectClass(helloClass).getDeclaredMethods().length))

	def test_compile_whenError(self):
		with self.assertRaisesRegex(CompilationException, "Unable to compile the source"):
			javaCompile([("org.mdkt.HelloClass", self.getResourceAsString("compile_whenError/HelloClass.java"))])["org.mdkt.HelloClass"]

	def test_compile_WhenFailOnWarnings(self):
		with self.assertRaises(CompilationException):
			javaCompile([("org.mdkt.HelloClass", self.getResourceAsString("compile_WhenFailOnWarnings/HelloClass.java"))])["org.mdkt.HelloClass"]

	def test_compile_WhenIgnoreWarnings(self):
		helloClass = javaCompile(
			[("org.mdkt.HelloClass", self.getResourceAsString("compile_WhenIgnoreWarnings/HelloClass.java"))],
			ignoreWarnings=True
		)["org.mdkt.HelloClass"]
		res = helloClass().hello()
		self.assertEqual(0, res.size())

	def test_compile_WhenWarningsAndErrors(self):
		with self.assertRaises(CompilationException):
			try:
				javaCompile([("org.mdkt.HelloClass", self.getResourceAsString("compile_WhenWarningsAndErrors/HelloClass.java"))])["org.mdkt.HelloClass"]
			except Exception as e:
				print("Exception caught: {}", e)
				raise


if __name__ == "__main__":
	unittest.main()
