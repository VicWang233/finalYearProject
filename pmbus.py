#!/usr/bin/env python

# import the PyUSB module
import ftd2xx
import time
import sys
import linear_conversions


class PMBUS_COMMS:

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
        # set event notification
        # device.setEventNotification(ftd2xx.ftd2xx.EVENT_RXCHAR)

    def configuration_command(self, command):

        self.device.write(command + "\r\n")
        time.sleep(0.005)  # allow 5ms delay between the commands
        self.device.read(self.device.getQueueStatus())

    def process(self):

        # list devices by description, returns tuple of attached devices description strings
        d = ftd2xx.listDevices()
        print d

        try:
            self.device = ftd2xx.open(0)
            print self.device
        except ftd2xx.ftd2xx.DeviceError:
            print "Unable to open 'EM2130 device'."
            exit(1)

        self.set_up_device()

        self.configuration_command("t11001")  # configure trigger time
        self.configuration_command("t_020")  # configure trigger timeout
        self.configuration_command("is_07")  # i2c speed 400kHz
        self.configuration_command("ip_0")  # control pin off (device turned off)

        # read version
        self.device.write("v\r\n")
        time.sleep(0.005)

        if self.device.getQueueStatus() > 0:
            i = self.device.read(self.device.getQueueStatus())
            print "version = " + i[1:]

        #return self.device

        # send query
        # x = self.vout_query_command("iq_3f01028b")  # READ_VOUT
        # print x
        y = self.vin_query_command(self.device, "iq_3f010288")  # READ_VIN
        print y

    def vout_query_command(self, command):

        self.device.write(command + "\r\n")  # 3f is my slave address
        time.sleep(0.005)
        response = ""
        if self.device.getQueueStatus() > 0:
            response = self.device.read(self.device.getQueueStatus())
        res = response.rstrip()

        print "PMBus Response = 0x" + res[1:]
        a = response[-4:]
        b = response[1:3]
        a = a.rstrip()
        r = int("0x" + a + b, 0)
        print "Block command = 0x" + a + b

        x = linear_conversions.Linear_Convertions()
        result = x.L16_to_float(r)
        print "Result = " + str(result) + " V\n"
        return str(result)

    def vin_query_command(self, device, command):

        device.write(command + "\r\n")  # 3f is my slave address
        time.sleep(0.005)
        response = ""
        if device.getQueueStatus() > 0:
            response = device.read(device.getQueueStatus())
        res = response.rstrip()
        print "PMBus Response = 0x" + res[1:]
        a = response[-4:]
        b = response[1:3]
        a = a.rstrip()
        r = int("0x" + a + b, 0)
        print "Block command = 0x" + a + b

        x = linear_conversions.Linear_Convertions()
        result = x.L11_to_float(r)
        print "Result = %.2f" % result + " V\n"
        return str(result)


def main():
    s = PMBUS_COMMS()
    s.process()
    print('\nDone!')

if __name__ == '__main__':
    main()
