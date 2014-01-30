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


loop = GLib.MainLoop()

def on_finished(trans, exit):
    loop.quit()
    if exit != "exit-success":
        sys.exit(1)
        
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

if __name__ == "__main__":
    packages = sys.argv[1:]
    if packages:
        aptclient = AptClient()
        try:
            # Setting up transactions
            trans_update = aptclient.update_cache()
            trans_inst = aptclient.install_packages(packages)
            # Trigger on last transaction finished
            trans_inst.connect("finished", on_finished)
            # Chaining transactions
            trans_inst.run_after(trans_update)
            dia = AptProgressDialog(trans_update)
            dia.run(close_on_finished=True, show_error=True,
                    reply_handler=lambda: True,
                    error_handler=on_error,
                    )
        except Exception as error:
            print error
            loop.quit()
        loop.run()
    else:
        print("Usage: %s <package> [...]\nLicensed under the GNU General Public License, see http://www.gnu.org/licenses/gpl.html\nWritten by Schlomo Schapiro" % sys.argv[0])
        sys.exit(1)
