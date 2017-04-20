#####################################################################
#                                                                   #
#                           PMBusComms.py                           #
#                     Author: Angelika Kosciolek                    #
#                             05/03/2017                            #
#                                                                   #
#              Description: Set up PMBus communication              #
#                                                                   #
#####################################################################

import ftd2xx
import time
import LinearConversions
import re


class PMBusComms:

    def __init__(self):

        # list devices by description, returns tuple of attached devices description strings
        d = ftd2xx.listDevices()
        print d

        try:
            self.device = ftd2xx.open(0)
            print self.device
            self.set_up_device()

            self.configure_command(self.device, "t11001")  # configure trigger time
            self.configure_command(self.device, "t_020")  # configure trigger timeout
            self.configure_command(self.device, "is_07")  # i2c speed 400kHz
            self.configure_command(self.device, "ip_0")  # control pin off (device turned off)

            # read version
            time.sleep(0.005)
            self.device.write("v\r\n")
            time.sleep(0.005)

            if self.device.getQueueStatus() > 0:
                i = self.device.read(self.device.getQueueStatus())
                print "version = " + i[1:]
        except ftd2xx.ftd2xx.DeviceError:
            print "Unable to open 'EM2130 device'."
            self.device = ftd2xx.ftd2xx.DEVICE_NOT_FOUND

    def set_up_device(self):

        # set baud rate
        self.device.setBaudRate(1 * 1000 * 1000)
        # set data characteristics
        self.device.setDataCharacteristics(ftd2xx.ftd2xx.BITS_8, ftd2xx.ftd2xx.STOP_BITS_1, ftd2xx.ftd2xx.PARITY_NONE)
        # purge
        self.device.purge()
        # set RX/TX timeouts
        self.device.setTimeouts(300, 300)
        # set bit mode
        self.device.setBitMode(0xFF, 0x40)
        # set flow control
        self.device.setFlowControl(ftd2xx.ftd2xx.FLOW_NONE, 0, 0)
        # set chars
        self.device.setChars(0x0A, 0x7F, 0, 0)

    def configure_command(self, device, command):

        try:
            time.sleep(0.005)
            device.write(command + "\r\n")
            time.sleep(0.005)  # allow 5ms delay between the commands
            read = device.read(device.getQueueStatus())
            return read
        except:
            return "0.00"

    def l16_query_command(self, device,  command):

        try:
            time.sleep(0.005)
            device.write(command + "\r\n")  # 3f is my slave address
            time.sleep(0.005)
            response = ""
            if device.getQueueStatus() > 0:
                response = device.read(device.getQueueStatus())
            res = response.rstrip()

            #print "PMBus Response = 0x" + res[1:]
            a = response[-4:]
            b = response[1:3]
            a = a.rstrip()
            b = b.rstrip()
            if (re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", a) and
                    re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", b)):
                r = int("0x" + a + b, 0)
                #print "Block command = 0x" + a + b
                x = LinearConversions.LinearConversions()
                result = x.l16_to_float(r)
                #print "Result = " + str(result) + " V\n"
                val = ("%.2f" % result)
                return val
            else:
                time.sleep(0.005)
                device.write(command + "\r\n")  # 3f is my slave address
                time.sleep(0.005)
                response = ""
                if device.getQueueStatus() > 0:
                    response = device.read(device.getQueueStatus())
                res = response.rstrip()

                # print "PMBus Response = 0x" + res[1:]
                a = response[-4:]
                b = response[1:3]
                a = a.rstrip()
                b = b.rstrip()
                if (re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", a) and
                        re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", b)):
                    r = int("0x" + a + b, 0)
                    # print "Block command = 0x" + a + b
                    x = LinearConversions.LinearConversions()
                    result = x.l16_to_float(r)
                    # print "Result = " + str(result) + " V\n"
                    val = ("%.2f" % result)
                    return val
                else:
                    print("ERROR - Unvalid response\n")
                    return "0.0"
        except:
            if device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
                return "0.00"

    def l11_query_command(self, device, command):

        try:
            time.sleep(0.005)
            device.write(command + "\r\n")  # 3f is my slave address
            time.sleep(0.005)
            response = ""
            if device.getQueueStatus() > 0:
                response = device.read(device.getQueueStatus())
            res = response.rstrip()
            #print "PMBus Response = 0x" + res[1:]
            a = response[-4:]
            b = response[1:3]
            a = a.rstrip()
            b = b.rstrip()
            if (re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", a) and
                    re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", b)):
                r = int("0x" + a + b, 0)
                #print "Block command = 0x" + a + b
                x = LinearConversions.LinearConversions()
                result = x.l11_to_float(r)
                #print "Result = %.2f" % result + " V\n"
                val = ("%.2f" % result)
                return val
            else:
                time.sleep(0.005)
                device.write(command + "\r\n")  # 3f is my slave address
                time.sleep(0.005)
                response = ""
                if device.getQueueStatus() > 0:
                    response = device.read(device.getQueueStatus())
                res = response.rstrip()
                # print "PMBus Response = 0x" + res[1:]
                a = response[-4:]
                b = response[1:3]
                a = a.rstrip()
                b = b.rstrip()
                if (re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", a) and
                        re.match("([a-f][0-9]|[0-9][a-f]|[0-9][0-9]|[a-f][a-f])", b)):
                    r = int("0x" + a + b, 0)
                    # print "Block command = 0x" + a + b
                    x = LinearConversions.LinearConversions()
                    result = x.l11_to_float(r)
                    # print "Result = %.2f" % result + " V\n"
                    val = ("%.2f" % result)
                    return val
                else:
                    print("ERROR - Unvalid response\n")
                    return "0.0"
        except:
            if device == ftd2xx.ftd2xx.DEVICE_NOT_FOUND:
                return "0.00"

    def l11_write_command(self, device, command, value):

        try:
            x = LinearConversions.LinearConversions()
            result = x.float_to_l11(value)
            a = result[-2:]
            b = result[2:4]
            a = a.rstrip()
            b = b.rstrip()
            val = a + b
            time.sleep(0.005)
            device.write(command + val + "\r\n")
            time.sleep(0.005)  # allow 5ms delay between the commands
            device.read(device.getQueueStatus())
        except:
            print "no dev"

    def l16_write_command(self, device, command, value):

        try:
            x = LinearConversions.LinearConversions()
            result = x.float_to_l16(value)
            a = result[-2:]
            b = result[2:4]
            a = a.rstrip()
            b = b.rstrip()
            val = a + b
            time.sleep(0.005)
            device.write(command + val + "\r\n")
            time.sleep(0.005)  # allow 5ms delay between the commands
            device.read(device.getQueueStatus())
        except:
            print "no dev"

    def write_direct(self, device, command, hex_val):

        try:
            result = hex_val
            a = result[-2:]
            b = result[2:4]
            val = a + b
            cmd = str(command) + str(val) + "\r\n"
            time.sleep(0.005)
            device.write(cmd)
            time.sleep(0.005)  # allow 5ms delay between the commands
            device.read(device.getQueueStatus())
        except:
            print "no dev"


