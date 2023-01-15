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

MATH_FUNCTIONS = "sin|cos|tan|exp|log|log10|sqrt|pi|e|sinh|cosh|tanh|ceil|floor"


class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")

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

        text = line_edit.text().strip()
        # Check if input value is empty
        if not text:
            self.error_label.setText(
                f"Empty Input: please enter a valid input in {line_edit_name} "
            )
            self.error_label.show()
            return

        # validate with regular  expression
        invalid_input = re.sub(regular_exp, "", text)

        if invalid_input:
            self.error_label.setText(
                f"Invalid Input: The input '{invalid_input}' in {line_edit_name} is not valid, please enter a valid input",
            )
            self.error_label.show()
            return

        # check it it is a valid mathematical function
        if line_edit_name == "Function Input":
            try:
                x = np.linspace(
                    *map(
                        float,
                        [
                            self.min_x_input.text().strip(),
                            self.max_x_input.text().strip(),
                        ],
                    )
                )
                eval(line_edit.text().replace("^", "**"))
            except Exception as e:
                self.error_label.setText(
                    f"Invalid Mathematical function: The input '{text}' in {line_edit_name} is not valid, "
                )
                self.error_label.show()
                return

        self.error_label.hide()

    def plot(self):
        # Check Input Validation
        self.validate_input(self.range_re, self.max_x_input, "Max Input")
        self.validate_input(self.range_re, self.min_x_input, "Min Input")
        self.validate_input(self.function_re, self.function_input, "Function Input")

        if float(self.min_x_input.text().strip()) >= float(
            self.max_x_input.text().strip()
        ):
            self.validate_input(
                None, None, "Range Input", "Min value must be less than Max value"
            )

        if self.error_label.isVisible():
            return

        # Get user input for function and range
        self.function = self.function_input.text().strip()
        self.x_range = [
            self.min_x_input.text().strip(),
            self.max_x_input.text().strip(),
        ]

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
        ax.plot(x, y, label=rf"${self.function_input.text()}$")
        ax.legend()
        ax.grid()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.show()
    sys.exit(app.exec_())
