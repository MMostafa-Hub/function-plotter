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
)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
import re
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT,
)
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


class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setWindowIcon(QIcon("./icon.png"))
        self.setFixedSize(800, 600)

        # text input fields and plot button
        self.function_input = QLineEdit()
        self.min_x_input = QLineEdit()
        self.min_x_input.setFixedWidth(50)
        self.max_x_input = QLineEdit()
        self.max_x_input.setFixedWidth(50)
        self.plot_button = QPushButton("Plot")

        # regular expression to validate the input values
        self.range_re = r"^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"
        self.function_re = r"^[+\-*/\^%()\s0-9x\.eE|sin|cos|tan|exp|log|log10|sqrt|pi|e|sinh|cosh|tanh|ceil|floor|x]*$"

        # Input Layout for the form
        input_layout = QHBoxLayout()

        # Mathematical Function form
        input_layout.addWidget(QLabel("F(x) = "))
        self.function_input.setPlaceholderText("e.g. x^2 + x^3")
        input_layout.addWidget(self.function_input)

        # Range form
        input_layout.addWidget(QLabel("Range: ["))
        self.min_x_input.setText("-10")
        input_layout.addWidget(self.min_x_input)
        input_layout.addWidget(QLabel(", "))
        self.max_x_input.setText("10")
        input_layout.addWidget(self.max_x_input)
        input_layout.addWidget(QLabel("]"))

        # Adding the Plot button to the input layout
        input_layout.addWidget(self.plot_button)

        # Input Widget
        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        # bottom layout for the form and the error message
        bottom_layout = QVBoxLayout()

        # Add the input widget to the bottom layout
        bottom_layout.addWidget(input_widget)

        # Add error label to the bottom layout
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")
        self.error_label.hide()
        bottom_layout.addWidget(self.error_label)

        # Bottom Widget
        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)

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

        # Add navigation toolbar
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(bottom_widget)

        # make the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # if the user presses the enter key, we plot the function
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.plot()

    def validate_input(self):
        # we Validate the range first, if it is valid we validate the function
        if not self.validate_range():
            return False

        # Get user input for range
        self.raw_function = self.function_input.text().strip()

        # replace ** with ^ for convenience
        self.function = self.raw_function.replace("^", "**")

        # Check if input value is empty
        if not self.function:
            self.error_label.setText(
                f"Empty Input: The input in Function Input is empty, please enter a valid input",
            )
            self.error_label.show()
            return False

        # validate with regular  expression
        invalid_input = re.sub(self.function_re, "", self.raw_function)

        if invalid_input:
            self.error_label.setText(
                f"Invalid Input: The input '{invalid_input}' in function input is not valid, please enter a valid input",
            )
            self.error_label.show()
            return False

        # check it it is a valid mathematical function
        try:
            if self.function_input.text().strip().find("**") != -1:
                raise e
            x = np.linspace(*map(float, self.x_range))
            eval(self.function)
        except Exception as e:
            self.error_label.setText(
                f"Invalid Mathematical function: The input '{self.function}' in function input is not valid, please enter a valid input"
            )
            self.error_label.show()
            return False

        self.error_label.hide()

        return True

    def validate_range(self):
        # Get user input for range
        self.x_range = [
            self.min_x_input.text().strip(),
            self.max_x_input.text().strip(),
        ]

        # Check if input value is empty
        if not self.x_range[0] or not self.x_range[1]:
            self.error_label.setText(
                f"Empty Input: The input in Range Input is empty, please enter a valid input",
            )
            self.error_label.show()
            return False
        # Check if the range is valid
        try:
            if float(self.x_range[0]) >= float(self.x_range[1]):
                self.error_label.setText("Invalid Range: Min X must be less than Max X")
                self.error_label.show()
                return False

            # check if the input is a valid number
        except Exception as e:
            self.error_label.setText(
                f"Invalid Input: The input in Range is not valid, please enter a valid input",
            )
            self.error_label.show()
            return False
        return True

    def plot(self):
        # Check Input Validation
        if not self.validate_input():
            return

        # Plot the function
        x = np.linspace(*map(float, self.x_range))
        y = eval(self.function)

        # Handling the case where y is a scaler value
        if not isinstance(y, np.ndarray):
            y = np.array([y] * len(x))

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # add the latex form of the function to the plot
        ax.plot(x, y, label=rf"${self.function_input.text()}$")
        ax.legend()
        ax.grid()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.show()
    sys.exit(app.exec_())
