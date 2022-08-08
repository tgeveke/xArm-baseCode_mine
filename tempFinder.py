import math

import numpy as np

import csv


def temperatureFinder(inputReading, adcBits=0, adcMaxVoltage=0, pullupValue=100, vIn=3.3,
                      thermistorValuesFilename="thermistorCurve.csv"):
    """
    Gets the temperature of a thermistor given the voltage of a pulled-up analog input pin.

    :param inputReading: Value read by analog pin, V
    :param adcBits: Optional, leave 0 if passing in direct voltage. Assign a value to decode a raw ADC reading of the selected bit count
    :param adcMaxVoltage: Optional, only use if adcBits > 0
    :param pullupValue: Optional, default 100. Resistance of pullup resistor,kilhms
    :param vIn: Optional, default 3.3. Pullup voltage
    :param thermistorValuesFilename: Optional, default "thermistorCurve.csv". CSV file with temperatures (any unit) in the first column, and the corresponding thermistor resistances (kilohms) in the second.
    :return: The current temperature in the same units as provided in the thermistor value file.
    """

    # ADC
    if adcBits == 0:
        inputVoltage = inputReading
    else:
        inputVoltage = (inputReading / (math.pow(2, adcBits))) * adcMaxVoltage
    print(inputVoltage)
    # Get resistance of thermistor
    rTherm = (inputVoltage * pullupValue) / (vIn - inputVoltage)
    print("Thermistor reads %s kOhms" % rTherm)
    tempData = {}

    with open(thermistorValuesFilename, mode='r') as inp:
        reader = csv.reader(inp)
        tempData = {float(rows[1]): float(rows[0]) for rows in reader}
    print(tempData)
    resistances = tempData.keys()

    # Interpolate
    # Find key below current resistance
    lowerKey = -1
    for k in resistances:
        if k - rTherm <= 0:
            lowerKey = k
            break
    # Find key above current resistance
    higherKey = -1
    for k in reversed(resistances):
        if k - rTherm > 0:
            higherKey = k
            break

    lowerDiff = rTherm - lowerKey
    interRange = higherKey - lowerKey
    lowerTemp = tempData[lowerKey]
    tempRange = tempData[higherKey] - lowerTemp

    rangeFraction = lowerDiff / interRange
    temp = rangeFraction * tempRange + lowerTemp
    return round(temp, 2)
