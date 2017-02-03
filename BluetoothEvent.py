#!/usr/bin/env python

import rumps
import objc
import urllib, urllib2
import Foundation

INTERVAL = 10 * 60

def update_callback(name, address, state):
    pass

    # Upload status changes to slack
    #
    #payload = {
    #    "payload": {
    #        "text": "*{state}* (_{deviceName}_)".format(
    #            deviceName=name,
    #            state={ True: "Seated", False: "Away" }[state]),
    #        "mrkdwn": True
    #    }
    #}
    #
    #urllib2.urlopen("https://hooks.slack.com/services/<your/incoming-webhooks/url>",
    #    urllib.urlencode(payload)).read()

class BluetoothEvent(rumps.App):
    def __init__(self, interval, update_callback):
        super(BluetoothEvent, self).__init__("BluetoothEvent")

        # Load IOBluetooth.framework
        self.iobluetooth = objc.ObjCLazyModule(
            "IOBluetooth",
            frameworkIdentifier="com.apple.IOBluetooth",
            frameworkPath=objc.pathForFramework("/System/Library/Frameworks/IOBluetooth.framework"),
            metadict=globals())

        # Setup menubar icon (https://github.com/google/material-design-icons)
        if not Foundation.NSUserDefaults.standardUserDefaults().objectForKey_("AppleInterfaceStyle"):
            self.icon = "ic_phonelink_black_24dp.png"
        else:
            self.icon = "ic_phonelink_white_24dp.png"

        # Prepare menu items for each devices
        self.devices = {}
        for device in self.iobluetooth.IOBluetoothDevice.pairedDevices():
            self.devices[device.addressString()] = (
                rumps.MenuItem(device.name(), callback=self.switch_callback),
                device.name(),
                False
            )

        for item, name, previous in sorted(self.devices.values(), key=lambda x: x[1]):
            self.menu.add(item)

        self.menu.add(rumps.separator)

        # Setup timer
        self.timer = rumps.Timer(self.timer_callback, interval)
        self.timer.start()

        self.update_callback = update_callback

    def switch_callback(self, item):
        item.state = not item.state

    def timer_callback(self, timer):
        for address, value in filter(lambda x: x[1][0].state, self.devices.items()):
            self.check(address)

    def check(self, address):
        item, name, previous = self.devices[address]

        device = self.iobluetooth.IOBluetoothDevice.deviceWithAddressString_(address)
        current = device.openConnection() == 0
        if current:
            device.closeConnection()

        if current != previous:
            self.devices[address] = (item, name, current)
            print("{} ({}): {}".format(name, address, str(current)))
            self.update_callback(name, address, current)

if __name__ == "__main__":
    BluetoothEvent(INTERVAL, update_callback).run()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
