import re
import json
from typing import List, Tuple


def getFloatValue(value: float) -> str:
    """
    Get the float value of an input value
    ie, 1.01 will return 01 as a string
    """
    _, floatingValue = str(value).split('.')
    return floatingValue

def getFloatPrecision(value: float) -> int:
    """
    Get the float precision of an input value
    """
    return len(getFloatValue(value))

def formatFloat(value: float, precision: int):
    """
    Format a float with a provided precision with some goodies
    Format to the provided precision, except:
    * If precision is zero, bump it to 1
    * If precision value is zero, default to 0
    """
    floatingValue = getFloatValue(value)

    if precision == 0:
        precision = 1

    if floatingValue == '0':
        precision = 0;
        value = int(value)

    return round(value, precision)


def buildConvertionStr(ogTuple: Tuple[str, float], convTuple: Tuple[str, float]) -> str:
    """
    Builds a conversion string segment given an original match and converted tuple
    Returns a string formated similar to "0.0c is 32.0f"
    """
    messageTemplate = '{ogVal}{ogUnit} is {convVal}{convUnit}'

    ogVal, ogUnit = ogTuple
    convVal, convUnit = convTuple

    floatPrecision = getFloatPrecision(ogVal)

    convVal = formatFloat(convVal, floatPrecision)
    ogVal = formatFloat(ogVal, floatPrecision)


    return messageTemplate.format(ogVal=ogVal, ogUnit=ogUnit, convVal=convVal, convUnit=convUnit)

def getConversionTupleFromMessage(msg: str) -> List[Tuple[str, float]]:
    """
    Given a message, builds Conversion Tuples
    Returns a list of conversion tuples (str, float)
    """
    validUnits = "|".join(CONVERSION_MAP.keys())
    conversionReg = re.compile(r'(?:^| )(?P<value>-?\d+(\.\d+)?) ?(?P<unit>%s)(?:(?= )|\W|$)' % validUnits, re.IGNORECASE)
    matches = conversionReg.finditer(msg)

    return list(map(reMatchToTuple, matches))

def reMatchToTuple(match) -> Tuple[float, str]:
    """
    Given a regexp match object builds a conversion tuple
    Returns a tuple (str, float)
    """
    if not match:
        return

    val = float(match.group('value'))
    unit = match.group('unit').lower()

    return (val, unit)

def convertMatch(convTuple: Tuple[float, str]) -> Tuple[float, str]:
    """
    Given a conversion tuple, convert it
    Returns a tuple of (original, converted) tuples
    """
    val, unit = convTuple

    conversionFunc = CONVERSION_MAP.get(unit)
    if not conversionFunc:
        return

    return (convTuple, conversionFunc(val))

def convertFahrenheitToCelsius(fahrenheit: float) -> Tuple[float, str]:
    """
    Converts fahrenheit to celsius
    Returns (celsius, unit)
    """
    return ((fahrenheit - 32) / 1.8, 'c')

def convertKelvinToCelsius(kelvin: float) -> Tuple[float, str]:
    """
    Converts kelvin to celsius
    Returns (kelvin, unit)
    """
    return (kelvin - 273.15, 'c')

def convertCelsiusToFahrenheit(celsius: float) -> Tuple[float, str]:
    """
    Converts celsius to fahrenheit
    Returns (fahrenheit, unit)
    """
    return (celsius * 1.8 + 32, 'f')

def convertKilogramsToPounds(kilogram: float) -> Tuple[float, str]:
    """
    Converts kilogram to pounds.
    Return (pounds, unit)
    """
    return (kilogram * 2.205, 'lb')

def convertPoundsToKilograms(pound: float) -> Tuple[float, str]:
    """
    Converts pounds to kilogram.
    Return (kilograms, unit)
    """
    return (pound / 2.205, 'kg')

def convertLiterToGallon(liter: float) -> Tuple[float, str]:
    """
    Converts liter to gallon.
    Return (gallon, unit)
    """
    return (liter * 0.264172, 'gal')

def convertGallonToLiter(gallon: float) -> Tuple[float, str]:
    """
    Converts gallon to liter.
    Return (liter, unit)
    """
    return (gallon / 0.264172, 'l')

def notImplemented():

    """
    Returns None
    """
    return None

CONVERSION_MAP = {
    'f': convertFahrenheitToCelsius,
    'c': convertCelsiusToFahrenheit,
    'kelvin': convertKelvinToCelsius,
    'kg': convertKilogramsToPounds,
    'lb': convertPoundsToKilograms,
    'l': convertLiterToGallon,
    'gal': convertGallonToLiter
}
