"""
originally from: https://bitbucket.org/zunzuncode/ramanspectroscopyfit
modified by <gsec 2018>
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, differential_evolution


def run_fit(xData, yData):
    # Double Lorentzian peak function
    # bounds on parameters are set in generate_Initial_Parameters() below

    def fit_func(x, a, b, A0, w0, x0, A1, w1, x1):
        return (
            a
            + x * b
            + (2 * A0 / np.pi) * (w0 / (4 * (x - x0) ** 2 + w0 ** 2))
            + (2 * A1 / np.pi) * (w1 / (4 * (x - x1) ** 2 + w1 ** 2))
        )

    # function for genetic algorithm to minimize (sum of squared error)
    # bounds on parameters are set in generate_Initial_Parameters() below
    def sumOfSquaredError(parameterTuple):
        return np.sum((yData - fit_func(xData, *parameterTuple)) ** 2)

    def generate_Initial_Parameters():
        # min and max used for bounds
        maxX = max(xData)
        minX = min(xData)
        maxY = max(yData)
        minY = min(yData)

        parameterBounds = []
        parameterBounds.append([-1.0, 1.0])                     # offset
        parameterBounds.append([maxY / -2.0, maxY / 2.0])       # tilt
        parameterBounds.append([maxY / 10.0, maxY * 1000.0])    # A0
        parameterBounds.append([0.0, maxX / 2.0])               # w0
        parameterBounds.append([minX, maxX])                    # x0
        parameterBounds.append([maxY / 10.0, maxY * 1000.0])    # A1
        parameterBounds.append([0.0, maxX / 2.0])               # w1
        parameterBounds.append([minX, maxX])                    # x1

        result = differential_evolution(sumOfSquaredError, parameterBounds)
        return result.x

    # generate initial parameter values
    initialParameters = generate_Initial_Parameters()

    # curve fit the test data
    fittedParameters, pcov = curve_fit(fit_func, xData, yData, p0=initialParameters)

    # create values for display of fitted peak function
    a, b, A0, w0, x0, A1, w1, x1 = fittedParameters
    y_fit = fit_func(xData, a, b, A0, w0, x0, A1, w1, x1)

    return y_fit, fittedParameters
