# BluetoothEvent

Status bar app for Mac OS X.
This is simple app to invoke your Python code when Bluetooth connection status is changed.

## Requirements

* Python 2.7.x
* Git
* Mercurial (hg)

## Dependencies

Dependencies will be resolved automatically by `setup_requires` keyword of [setuptools](https://setuptools.readthedocs.io/en/latest/).
 
* [rumps](https://github.com/jaredks/rumps)
* [py2app](https://bitbucket.org/ronaldoussoren/py2app)

## Configure

You can modify device list (`DEVICES`), checking interval (`INTERVAL`) and callback (`update_callback`).
There are defined in [BluetoothEvent.py](https://github.com/lostman-github/BluetoothEvent/blob/master/BluetoothEvent.py).

* DEVICES (default is empty)
  * Target device name and address.
* INTERVAL (default is 10min)
  * Interval time in sec.
* update_callback (default is pass)
  * Callback function which is invoked when connection status is changed.
  * Device name and status (connected or not) will be passed from this app.

## Build

Note.
If you have use Python with pyenv, you need to reinstall Python with framework option.
Please check [this instruction](https://github.com/yyuu/pyenv/wiki#how-to-build-cpython-with-framework-support-on-os-x).

You can clone and build `BluetoothEvent.app` with following commands.
(This commands does NOT install any files to your system.
Compiled files and depends packages will be saved to working directory.)

```
$ git clone https://github.com/lostman-github/BluetoothEvent.git
$ cd BluetoothEvent
$ python setup.py py2app
```

`BluetoothEvent.app` will be created in `dist` directory, if build process is successful.

## Run

Run `BluetoothEvent.app`. (or run `./dist/BluetoothEvent.app/Contents/MacOS/BluetoothEvent` in your terminal.)
New icon will appear in status bar.
Your devices are appeared as menu item in menu of status icon.
When you click device name, clicked item will be marked as checked.
In next interval, this app will check connection status of checked devices.
If status is changed, `update_callback` will be called.
