# Function Plotter

Function Plotter is a simple and easy to use app for plotting mathematical functions. It uses PySide2, Matplotlib and numpy libraries to create the plots.

## Features

-   Plot a wide range of mathematical functions such as trigonometric, exponential, logarithmic, and hyperbolic functions
-   Input functions using mathematical notation, e.g. "x^2 + x^3"
-   Set custom X-axis range for the plot
-   Show and Export the plot as an image

## Installation

To use Function Plotter, you will need Python 3 and the following dependencies:

-   PySide2
-   Matplotlib
-   Numpy

You can install these using pip:
```
pip install PySide2 matplotlib numpy
```

## Usage

1.  Input the mathematical function you want to plot in the "F(x)" field.
2.  Set the X-axis range by entering the minimum and maximum values in the "Range" field.
3.  Click the "Plot" button or hit Enter to generate the plot.
4.  To export the plot as an image, click the Save Button on the main toolbar.

## Examples

### Working Examples
-   Plotting the function "x^2 + x^3":
    -   Input: "x^2 + x^3"
    -   Range: [-10, 10]
	<img title="working example 1" alt="Alt text" src="/Examples/working1.JPG">

-   Plotting the sine function:
    -   Input: "sin(x)"
    -   Range: [0, 10]
	<img title="working example 2" alt="Alt text" src="/Examples/working2.JPG">
### Wrong Examples
-   Plotting the function "x**3":
    -   Input: "x**3"
    -   Range: [-10, 10]
	<img title="working example 1" alt="Alt text" src="/Examples/wrong1.JPG">

-   Plotting the sine function:
    -   Input: "sin(x)"
    -   Range: [0, 2*pi]
	<img title="working example 2" alt="Alt text" src="/Examples/wrong2.JPG">
## License
Function Plotter is released under the [MIT License](https://opensource.org/licenses/MIT). This means that you are free to use, modify, and distribute the software as long as you include the original copyright and license notice in any copies.
