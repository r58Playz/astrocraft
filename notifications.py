"""
Based on a solution for Linux(https://help.gnome.org/users/zenity/3.24/notification.html.en), and a solution for MacOS(https://stackoverflow.com/questions/17651017/python-post-osx-notification)
"""

# standard library
import threading
import os
import platform

import globals as G

class ToastNotifier(object):
    """Create a toast notification.
    """

    def __init__(self):
        """Initialize."""
        self._thread = None

    def _show_toast(self,msg, duration):
        """Notification settings.
        :title: notification title
        :msg: notification message
        :icon_path: path to the .ico file to custom notification
        :duration: delay in seconds before notification self-destruction
        """
        if platform.platform() == "Windows":
           print(msg)  # TODO: add support for windows
        elif platform.platform() == "Darwin":  # macos
            os.system("""
                      osascript -e 'display notification "{}" with title "{}"'
                      """.format(msg, G.APP_NAME))  # TODO: add icon support
            return None
        elif platform.platform() == "Linux":
            import subprocess
            cmd = 'zenity --notification --text="' + (G.APP_NAME + ': ' + msg + '"')
            subprocess.check_call([cmd])
        return None

    def show_toast(self, msg, duration=5, threaded=False):
        """Notification settings.
        :title: notification title
        :msg: notification message
        :duration: delay in seconds before notification self-destruction
        """
        if not threaded:
            self._show_toast(msg, duration)
        else:
            if self.notification_active():
                # We have an active notification, let is finish so we don't spam them
                return False

            self._thread = threading.Thread(target=self._show_toast, args=(msg, duration))
            self._thread.start()
        return True

    def notification_active(self):
        """See if we have an active notification showing"""
        if self._thread != None and self._thread.is_alive():
            # We have an active notification, let is finish we don't spam them
            return True
        return False

G.NOTIFICATIONS = ToastNotifier()
