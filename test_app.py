import pytest
from app import FunctionPlotter
from PySide2 import QtCore


@pytest.fixture
def function_plotter(qtbot):
    plotter = FunctionPlotter()
    qtbot.addWidget(plotter)
    plotter.show()
    return plotter


def test_validate_function_input(function_plotter):
    plotter = function_plotter

    # since we test only the function input, we need to set a valid range
    plotter.max_x_input.setText("100")
    plotter.min_x_input.setText("10")

    # test for variable
    plotter.function_input.setText("x")
    assert plotter.validate_input() == True

    plotter.function_input.setText("d")
    assert plotter.validate_input() == False

    plotter.function_input.setText("d^3")
    assert plotter.validate_input() == False

    # testing for mathematical functions
    plotter.function_input.setText("log(x)")
    assert plotter.validate_input() == True

    plotter.function_input.setText("sin(x)")
    assert plotter.validate_input() == True

    plotter.function_input.setText("cotan(x)")
    assert plotter.validate_input() == False

    # testing for operators
    plotter.function_input.setText("x*2")
    assert plotter.validate_input() == True

    plotter.function_input.setText("x**2")
    assert plotter.validate_input() == False

    plotter.function_input.setText("^x")
    assert plotter.validate_input() == False


def test_validate_range_input(function_plotter, qtbot):
    plotter = function_plotter

    # since we test only the range input, we need to set a valid function
    plotter.function_input.setText("x")

    # test for valid range
    plotter.min_x_input.setText("-10")
    plotter.max_x_input.setText("10")
    qtbot.mouseClick(plotter.plot_button, QtCore.Qt.LeftButton)

    # check if the start and the end of the plot is correct
    assert plotter.canvas.figure.axes[0].lines[0].get_xdata()[0] == -10
    assert plotter.canvas.figure.axes[0].lines[0].get_xdata()[-1] == 10

    # test for different ranges
    plotter.min_x_input.setText("10")
    plotter.max_x_input.setText("-10")
    assert plotter.validate_range() == False

    plotter.min_x_input.setText("d")
    plotter.max_x_input.setText("-10")
    assert plotter.validate_range() == False

    plotter.min_x_input.setText("2")
    plotter.max_x_input.setText("4^10")
    assert plotter.validate_range() == False

    plotter.min_x_input.setText("0")
    plotter.max_x_input.setText("0")
    assert plotter.validate_range() == False

    plotter.min_x_input.setText("-1")
    plotter.max_x_input.setText("0")
    assert plotter.validate_range() == True
