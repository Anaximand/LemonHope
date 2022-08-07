import re
import json
from typing import Tuple



def buildConvertionSegment(ogTuple: Tuple[str, float], convTuple: Tuple[str, float]) -> str:
        messageTemplate = '{ogVal:.1f}{ogUnit} is {convVal:.1f}{convUnit}'

        ogVal, ogUnit = ogTuple
        convVal, convUnit = convTuple

        return messageTemplate.format(ogVal=ogVal, ogUnit=ogUnit, convVal=convVal, convUnit=convUnit)

def getConversionTupleFromMessage(msg: str):
    conversionReg = re.compile(r'(?P<value>\d+\.?(\d+)?)(?P<unit>\w{1,2})')
    return conversionReg.finditer(msg)

def reMatchToTuple(match) -> Tuple[str, float]:
    if not match:
        return

    val = float(match.group('value'))
    unit = match.group('unit')

    return (val, unit)

def convertMatch(matchTuple: Tuple[float, str]) -> Tuple[float, str]:
    val, unit = matchTuple

    conversionFunc = CONVERSION_MAP.get(unit)
    if not conversionFunc:
        return

    return conversionFunc(val)

def convertFahrenheitToCelsius(fahrenheit: float) -> Tuple[float, str]:
    return ((fahrenheit - 32) / 1.8, 'c')

def convertCelsiusToFahrenheit(celsius: float) -> Tuple[float, str]:
    return (celsius * 1.8 + 32, 'f')

def notImplemented():
    return None

CONVERSION_MAP = {
    'f': convertFahrenheitToCelsius,
    'c': convertCelsiusToFahrenheit,
    'lb': notImplemented,
    'kg': notImplemented,
    'km': notImplemented,
    'mi': notImplemented,
    'in': notImplemented,
    'cm': notImplemented,
    'm': notImplemented,
}
