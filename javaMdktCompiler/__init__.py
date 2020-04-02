__all__ = ("javaCompile",)
import typing
from pathlib import Path

from JAbs import SelectedJVMInitializer

mdktNS = "org.mdkt.compiler"

neededMdktCompilerClasses = [
	mdktNS + ".InMemoryJavaCompiler",
	mdktNS + ".SourceCode",
	mdktNS + ".CompilationException",
]

defaultBaseDir = Path(".")


def getMDKTCompilerPath(baseDir=None):
	if baseDir is None:
		baseDir = defaultBaseDir

	candidates = sorted(defaultBaseDir.glob("InMemoryJavaCompiler-*.jar"))
	if not candidates:
		candidates = sorted(defaultBaseDir.glob("org.mdkt.compiler-*.jar"))

	return candidates[-1]


MDKTCompilerClassPath = getMDKTCompilerPath()
ji = SelectedJVMInitializer([MDKTCompilerClassPath], neededMdktCompilerClasses)
CompilationException = ji.CompilationException

def javaCompile(filesAbstracted: typing.Iterable[typing.Union[typing.Tuple[str, str], Path]], *args, compiler=None, ignoreWarnings:bool=False):
	if compiler is None:
		compiler = ji.InMemoryJavaCompiler.newInstance()
		if ignoreWarnings:
			compiler.ignoreWarnings()

	compiler.useOptions(args)

	for it in filesAbstracted:
		if isinstance(it, Path):
			fileStem = it.stem
			fileText = it.read_text(encoding="utf-8")
		else:
			fileStem, fileText = it
		compiler.addSource(fileStem, fileText)

	compiledN = compiler.compileAll()
	compiled = {}
	for k in compiledN:
		compiled[str(k)] = ji.reflClass2Class(compiledN[k])
	return compiled
