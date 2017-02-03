#!/usr/bin/env python

import rumps
import objc
import urllib, urllib2
import Foundation

INTERVALS = [
    #("5 Seconds", 5),
    ("1 Minutes", 1 * 60),
    ("2 Minutes", 2 * 60),
    ("5 Minutes", 5 * 60),
    ("10 Minutes", 10 * 60),
    ("20 Minutes", 20 * 60),
    ("30 Minutes", 30 * 60),
]

def update_callback(name, address, state):
    print("{} ({}): {}".format(name, address, str(state)))

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
    def __init__(self, intervals, update_callback):
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

        # Setup timer
        self.timer = None

        self.menu.add(rumps.MenuItem("Intervals"))

        self.intervals = {}
        for title, value in intervals:
            item = rumps.MenuItem(title, callback=self.interval_menu_callback)
            self.intervals[title] = (
                item,
                value
            )
            self.menu.add(item)

        self.menu.add(rumps.separator)

        # Prepare menu items for each devices
        self.menu.add(rumps.MenuItem("Devices"))

        self.devices = {}
        for device in self.iobluetooth.IOBluetoothDevice.pairedDevices():
            self.devices[device.addressString()] = (
                rumps.MenuItem(device.name(), callback=self.device_menu_callback),
                device.name(),
                False
            )

        for item, name, previous in sorted(self.devices.values(), key=lambda x: x[1]):
            self.menu.add(item)

        self.menu.add(rumps.separator)

        # Setup update callback
        self.update_callback = update_callback

    def interval_menu_callback(self, item):
        item.state = not item.state

        for title, value in filter(lambda x: x[0] != item.title, self.intervals.items()):
            value[0].state = False

        if self.timer and self.timer.is_alive():
            self.timer.stop()

        if item.state:
            self.timer = rumps.Timer(self.timer_callback, self.intervals[item.title][1])
            self.timer.start()

    def timer_callback(self, timer):
        for address, value in filter(lambda x: x[1][0].state, self.devices.items()):
            self.check(address)

    def device_menu_callback(self, item):
        item.state = not item.state

    def check(self, address):
        item, name, previous = self.devices[address]

        device = self.iobluetooth.IOBluetoothDevice.deviceWithAddressString_(address)
        current = device.openConnection() == 0
        if current:
            device.closeConnection()

        if current != previous:
            self.devices[address] = (item, name, current)
            self.update_callback(name, address, current)

if __name__ == "__main__":
    BluetoothEvent(INTERVALS, update_callback).run()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
