#!/usr/bin/env python
import math
import ctypes


def L11_to_float(input_val):

    e = ctypes.c_int8(input_val >> 11)
    m = ctypes.c_int16(input_val & 0x7ff)
    if e.value > 0x0F:
        e.value |= 0xE0
    if m.value > 0x03FF:
        m.value |= 0xF800
    return m.value * pow(2, e.value)


def float_to_L11(input_val):
    exponent = -16
    mantissa = int(input_val/math.pow(2.0, exponent))

    while exponent < 15:
        if mantissa >= -1024 and mantissa <= 1023:
            break
        exponent = exponent + 1
        mantissa = int(input_val / math.pow(2.0, exponent))

    uExponent = ctypes.c_uint16(exponent << 11)
    uMantissa = ctypes.c_uint16(mantissa & 0x07FF)
    value = uExponent.value | uMantissa.value
    return hex(value)


# L16 USING FOR VOUT COMMANDS!!!
def L16_to_float(input_val):
    e = ctypes.c_int8(-13)  # my device uses exp = -13
    m = ctypes.c_int16(input_val)
    #if e.value > 0x0F:
        #e.value |= 0xE0
    #if m.value > 0x03FF:
        #m.value |= 0xF800
    return m.value * pow(2, e.value)


def float_to_L16(input_val):
    L16_length = -13  # -13 always for our device
    exponent = math.pow(2.0, L16_length)
    value = int(input_val/exponent)
    return hex(value)


def main():
    n = L11_to_float(0xDA03)  # working ok
    m = float_to_L11(16.1)  # working ok
    i = L16_to_float(0x2105)  # working ok
    p = float_to_L16(2.564)  # working ok
    print i

if __name__ == '__main__':
    main()
