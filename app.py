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
from PySide2.QtCore import Qt
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

        # text input fields and plot button
        self.function_input = QLineEdit()
        self.x_range_input = QLineEdit()
        self.plot_button = QPushButton("Plot")

        # Layout for the form
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Enter a mathematical function (e.g. x**2): "))
        main_layout.addWidget(self.function_input)
        main_layout.addWidget(
            QLabel("Enter the range of x-values to plot (e.g. -10, 10): ")
        )
        main_layout.addWidget(self.x_range_input)

        # layout for the button (to the right of the form)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.plot_button)

        # adding the button layout to the main layout
        main_layout.addLayout(btn_layout)

        # make the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # connecting the push button signal to the plot slot
        self.plot_button.clicked.connect(self.plot)

    def plot(self):
        # Get user input for function and range
        self.function = self.function_input.text()
        self.x_range = self.x_range_input.text()

        # replace ** with ^ for convenience
        self.function = self.function.replace("^", "**")

        # Plot the function
        x = np.linspace(*map(float, self.x_range.split(",")))
        y = eval(self.function)

        plt.plot(x, y)
        plt.grid()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.show()
    sys.exit(app.exec_())
