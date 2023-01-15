import sys
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
)
import re
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

# importing all trigonometric, exponential, logarithmic, and hyperbolic functions
from numpy import (
    sin,
    cos,
    tan,
    exp,
    log,
    log10,
    sqrt,
    pi,
    e,
    sinh,
    cosh,
    tanh,
    ceil,
    floor,
)

MATH_FUNCTIONS = "sin|cos|tan|exp|log|log10|sqrt|pi|e|sinh|cosh|tanh|ceil|floor"


class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")

        # text input fields and plot button
        self.function_input = QLineEdit()
        self.min_x_input = QLineEdit()
        self.max_x_input = QLineEdit()
        self.plot_button = QPushButton("Plot")

        # regular expression to validate the input values
        self.range_re = r"^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"
        self.function_re = r"^[+\-*/\^%()\s0-9xX\.eE|" + MATH_FUNCTIONS + "]*$"

        # Input Layout for the form
        input_layout = QHBoxLayout()

        # Mathematical Function form
        input_layout.addWidget(QLabel("F(x) = "))
        self.function_input.setPlaceholderText("e.g. x^2 + x^3")
        input_layout.addWidget(self.function_input)

        # Range form
        input_layout.addWidget(QLabel("Range: ["))
        self.min_x_input.setPlaceholderText("-10")
        input_layout.addWidget(self.min_x_input)
        input_layout.addWidget(QLabel(", "))
        self.max_x_input.setPlaceholderText("10")
        input_layout.addWidget(self.max_x_input)
        input_layout.addWidget(QLabel("]"))

        input_layout.addWidget(self.plot_button)

        # Input Widget
        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        # connecting the push button signal to the plot slot
        self.plot_button.clicked.connect(self.plot)

        # Create figure for the plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # making an empty plot for good looks
        self.figure.add_subplot(111)
        self.canvas.draw()

        # Main Layout for the form and the plot
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(input_widget)

        # make the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def validate_input(self, regular_exp, line_edit, line_edit_name):
        text = line_edit.text().strip()

        # Check if input value is empty
        if not text:
            print(text)
            QMessageBox.warning(
                self,
                "Empty Value",
                f"please enter a valid input in {line_edit_name} ",
            )
        # validate with regular  expression
        invalid_input = re.sub(regular_exp, "", text)

        if invalid_input:
            QMessageBox.warning(
                self,
                "Invalid Input",
                f"The input '{invalid_input}' in {line_edit_name} is not valid, please enter a valid input",
            )

    def plot(self):
        # Check Input Validation
        self.validate_input(self.range_re, self.max_x_input, "Max Input")
        self.validate_input(self.range_re, self.min_x_input, "Min Input")
        self.validate_input(self.function_re, self.function_input, "Function Input")

        # Get user input for function and range
        self.function = self.function_input.text()
        self.x_range = [self.min_x_input.text(), self.max_x_input.text()]

        # replace ** with ^ for convenience
        self.function = self.function.replace("^", "**")

        # Plot the function
        x = np.linspace(*map(float, self.x_range))
        y = eval(self.function)

        # Handling the case where y is a scaler value
        if not isinstance(y, np.ndarray):
            y = np.array([y] * len(x))

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.show()
    sys.exit(app.exec_())
