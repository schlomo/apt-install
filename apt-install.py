#!/usr/bin/env python
"""
One-step update apt cache and install packages
"""
# based on http://pythonhosted.org/aptdaemon/dbus.html and on http://bazaar.launchpad.net/~aptdaemon-developers/aptdaemon/main/view/head:/gtk3-demo.py
import sys

from gi.repository import GLib


from aptdaemon.client import AptClient

from aptdaemon.gtk3widgets import AptErrorDialog, AptConfirmDialog, AptProgressDialog
import aptdaemon.errors
from aptdaemon.enums import *


loop = GLib.MainLoop()
aptclient = AptClient()
packages=[]

def on_error(error):
    if isinstance(error, aptdaemon.errors.NotAuthorizedError):
        # Silently ignore auth failures
        return
    elif not isinstance(error, aptdaemon.errors.TransactionFailed):
        # Catch internal errors of the client
        error = aptdaemon.errors.TransactionFailed(ERROR_UNKNOWN,str(error))
    dia = AptErrorDialog(error)
    dia.run()
    dia.hide()

def on_finished_update(trans, exit):
    GLib.timeout_add(200,do_install)
    return True

def do_update():
    trans_update = aptclient.update_cache()
    trans_update.connect("finished",on_finished_update)
    
    dia = AptProgressDialog(trans_update)
    dia.run(close_on_finished=True, show_error=True,
            reply_handler=lambda: True,
            error_handler=on_error,
            )
    return False


def on_finished_install(trans, exit):
    loop.quit()
    if exit != "exit-success":
        sys.exit(1)

def do_install():
    trans_inst = aptclient.install_packages(packages)
    trans_inst.connect("finished", on_finished_install)
    dia2 = AptProgressDialog(trans_inst)
    dia2.run(close_on_finished=True, show_error=True,
                    reply_handler=lambda: True,
                    error_handler=on_error,
                    )
    return False
    

if __name__ == "__main__":
    packages = sys.argv[1:]
    if packages:
        GLib.timeout_add(50,do_update)
        loop.run()
    else:
        print("""Usage: %s <package> [...]
Licensed under the GNU General Public License, see http://www.gnu.org/licenses/gpl.html
Written by Schlomo Schapiro, see https://github.com/schlomo/apt-install""" % sys.argv[0])
        sys.exit(1)
