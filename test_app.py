import app as function_plotter
from PySide2 import QtCore
import pytest


@pytest.fixture
def app(qtbot):
    test_function_plotter = function_plotter.FunctionPlotter()
    qtbot.addWidget(test_function_plotter)
    return test_function_plotter


def test_range_input(app, qtbot):
    # +ve int, +ve int
    # -ve int, +ve int
    # +ve float, +ve int
    # +ve int, +ve int
    #
    pass


def test_mathematical_function_input(app, qtbot):
    pass
