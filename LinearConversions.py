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

    ###############################################################################################################
    #                                              L11 TO FLOAT                                                   #
    #                                                                                                             #
    #  Description: convert Linear Bit 11 to float value                                                          #
    #  Arguments: input_val (L11 value)                                                                           #
    #  Returns: float value                                                                                       #
    ###############################################################################################################

    def l11_to_float(self, input_val):

        # extract exponent as MS 5 bits
        exponent = ctypes.c_int8(input_val >> 11)
        # extract mantissa as LS 11 bits
        mantissa = ctypes.c_int16(input_val & 0x7ff)
        # sign extend exponent from 5 to 8 bits
        if exponent.value > 0x0F:
            exponent.value |= 0xE0
        # sign extend mantissa from 11 to 16 bits
        if mantissa.value > 0x03FF:
            mantissa.value |= 0xF800
        # compute and return value
        return mantissa.value * pow(2, exponent.value)

    ###############################################################################################################
    #                                              FLOAT TO L11                                                   #
    #                                                                                                             #
    #  Description: convert float to Linear Bit 11 value                                                          #
    #  Arguments: input_val (float)                                                                               #
    #  Returns: L11 value                                                                                         #
    ###############################################################################################################

    def float_to_l11(self, input_val):

        # set exponent to -16
        exponent = -16
        # extract mantissa from input value
        mantissa = int(input_val/math.pow(2.0, exponent))

        # search for an exponent that produces a valid 11-bit mantissa
        while exponent < 15:
            if -1024 <= mantissa <= 1023:
                break # stop if mantissa valid
            exponent += 1
            mantissa = int(input_val / math.pow(2.0, exponent))

        # format the exponent of the L11
        u_exponent = ctypes.c_uint16(exponent << 11)
        # format mantissa of the L11
        u_mantissa = ctypes.c_uint16(mantissa & 0x07FF)
        # compute and return value
        value = u_exponent.value | u_mantissa.value
        return hex(value)

    ###############################################################################################################
    #                                              L16 TO FLOAT                                                   #
    #                                                                                                             #
    #  Description: convert Linear Bit 16 to float value                                                          #
    #  -> L16 USED FOR VOUT COMMANDS <-                                                                           #
    #  Arguments: input_val (L16 value)                                                                           #
    #  Returns: float value                                                                                       #
    ###############################################################################################################

    def l16_to_float(self, input_val):

        # EM2130L uses exp = -13
        exponent = ctypes.c_int8(-13)
        mantissa = ctypes.c_uint16(input_val)
        # compute value and return
        return mantissa.value * pow(2, exponent.value)

    ###############################################################################################################
    #                                              FLOAT TO L16                                                   #
    #                                                                                                             #
    #  Description: convert float to Linear Bit 16 value                                                          #
    #  -> L16 USED FOR VOUT COMMANDS <-                                                                           #
    #  Arguments: input_val (float)                                                                               #
    #  Returns: L16 value                                                                                         #
    ###############################################################################################################

    def float_to_l16(self, input_val):

        # EM130L uses -13
        l16_length = -13
        # set exponent
        exponent = math.pow(2.0, l16_length)
        # compute and return value
        value = int(input_val/exponent)
        return hex(value)

###############################################################################################################
#                                              MAIN FUNCTION                                                  #
#                                                                                                             #
#  Description: function used to check Linear Conversions outside of the main application                     #
#  and print them on terminal                                                                                 #
#  Arguments: none                                                                                            #
#  Returns: none                                                                                              #
###############################################################################################################


def main():

    conv = LinearConversions()
    n = conv.l11_to_float(0xda03)  # working ok
    m = conv.float_to_l11(0)  # working ok
    i = conv.l16_to_float(0xca35)  # working ok
    p = conv.float_to_l16(7.75)  # working ok
    print n
    print m

    print i
    print p

if __name__ == '__main__':
    main()
