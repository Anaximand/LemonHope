import re
import json
from typing import List, Tuple


def buildConvertionStr(ogTuple: Tuple[str, float], convTuple: Tuple[str, float]) -> str:
    """
    Builds a conversion string segment given an original match and converted tuple
    Returns a string formated similar to "0.0c is 32.0f"
    """
    messageTemplate = '{ogVal:.1f}{ogUnit} is {convVal:.1f}{convUnit}'

    ogVal, ogUnit = ogTuple
    convVal, convUnit = convTuple

    return messageTemplate.format(ogVal=ogVal, ogUnit=ogUnit, convVal=convVal, convUnit=convUnit)

def getConversionTupleFromMessage(msg: str) -> List[Tuple[str, float]]:
    """
    Given a message, builds Conversion Tuples
    Returns a list of conversion tuples (str, float)
    """
    validUnits = "|".join(CONVERSION_MAP.keys())
    conversionReg = re.compile(r'(?P<value>\d+\.?(\d+)?)(?P<unit>%s)' % validUnits)
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
    unit = match.group('unit')

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

def convertCelsiusToFahrenheit(celsius: float) -> Tuple[float, str]:
    """
    Converts celsius to fahrenheit
    Returns (fahrenheit, unit)
    """
    return (celsius * 1.8 + 32, 'f')

def notImplemented():
    """
    Returns None
    """
    return None

CONVERSION_MAP = {
    'f': convertFahrenheitToCelsius,
    'c': convertCelsiusToFahrenheit,
}
