#####################################################################
#                                                                   #
#                        LinearConversions.py                       #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#     Description: Conversions needed to encode PMBus responses     #
#        Linear Bit 11 to float and Linear Bit 16 to float          #
#                                                                   #
#####################################################################

import math
import ctypes


class LinearConversions:

    def l11_to_float(self, input_val):

        exponent = ctypes.c_int8(input_val >> 11)
        mantissa = ctypes.c_int16(input_val & 0x7ff)
        if exponent.value > 0x0F:
            exponent.value |= 0xE0
        if mantissa.value > 0x03FF:
            mantissa.value |= 0xF800
        return mantissa.value * pow(2, exponent.value)

    def float_to_l11(self, input_val):

        exponent = -16
        mantissa = int(input_val/math.pow(2.0, exponent))

        while exponent < 15:
            if -1024 <= mantissa <= 1023:
                break
            exponent += 1
            mantissa = int(input_val / math.pow(2.0, exponent))

        u_exponent = ctypes.c_uint16(exponent << 11)
        u_mantissa = ctypes.c_uint16(mantissa & 0x07FF)
        value = u_exponent.value | u_mantissa.value
        return hex(value)

    # L16 USING FOR VOUT COMMANDS!!!
    def l16_to_float(self, input_val):

        exponent = ctypes.c_int8(-13)  # my device uses exp = -13
        mantissa = ctypes.c_int16(input_val)
        return mantissa.value * pow(2, exponent.value)

    def float_to_l16(self, input_val):
        l16_length = -13  # -13 always for our device
        exponent = math.pow(2.0, l16_length)
        value = int(input_val/exponent)
        return hex(value)


def main():
    conv = LinearConversions()
    n = conv.l11_to_float(0xDA03)  # working ok
    m = conv.float_to_l11(16.1)  # working ok
    i = conv.l16_to_float(0x2105)  # working ok
    p = conv.float_to_l16(2.564)  # working ok
    print i

if __name__ == '__main__':
    main()
