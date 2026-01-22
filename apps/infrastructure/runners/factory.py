from apps.domain.enums.language import Language
from apps.infrastructure.runners.python_runner import PythonRunner
from apps.infrastructure.runners.cpp_runner import CppRunner
from apps.infrastructure.runners.js_runner import JsRunner

class RunnerFactory:
    @staticmethod
    def create(language: str):
        lang = Language(language)
        if lang == Language.PYTHON:
            return PythonRunner()
        if lang == Language.CPP:
            return CppRunner()
        if lang == Language.JS:
            return JsRunner()
        raise ValueError("Unsupported language")
