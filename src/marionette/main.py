import os
import socketserver
import threading
import time
from marionette_driver.marionette import Marionette, HTMLElement


def run():
    """This needs to be wrapped in a function so marionette doesn't crash on clean-up"""
    binary_path = os.getenv('M_THUNDERBIRD_BIN', '/Applications/Thunderbird.app/Contents/MacOS/thunderbird')

    marionette = Marionette(app='thunderbird', bin=binary_path, headless=True, profile=os.getenv('M_THUNDERBIRD_PROFILE', '../../profiles/website'))

    session = marionette.start_session()
    print("Session -> ",session)

    marionette.set_context(marionette.CONTEXT_CHROME)
    # Set light-mode
    marionette.set_pref('extensions.activeThemeID', 'thunderbird-compact-light@mozilla.org')
    marionette.set_pref('browser.theme.content-theme', 1)
    marionette.set_pref('browser.theme.toolbar-theme', 1)

    # Enable userchrome
    marionette.set_pref('toolkit.legacyUserProfileCustomizations.stylesheets', True)
    # Enforce non-native titlebar buttons
    #marionette.set_pref('widget.gtk.non-native-titlebar-buttons.enabled', True)
    marionette.restart()

    marionette.set_window_rect(0, 0, 720, 1280)

    calendar_btn: HTMLElement = marionette.find_element('id', 'calendarButton')
    calendar_btn.click()

    time.sleep(1)

    # Dump screenshot into out.png
    with open('./calendar-screen.png', 'wb') as fh:
        marionette.save_screenshot(fh)

    # Click to activate start page
    tabs: list[HTMLElement] = marionette.find_elements('class name', 'tabmail-tab')
    tabs[0].click()

    # Wait until start page is loaded-ish
    #time.sleep(1)

    # Dump screenshot into out.png
    with open('./mail-screen.png', 'wb') as fh:
        marionette.save_screenshot(fh)

    marionette.delete_session()


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Hi!", self.client_address)
        data = str(self.request.recv(1024), 'ascii')
        print("Received: ", data)
        response = b'* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE AUTH=PLAIN AUTH=LOGIN] IMAP/POP3 ready - us11-012mip'
        print("Sending Response: ", response)
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = ('localhost', 14300)
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        print("Running Marionette...")
        run()
        print("Done!")

        server.shutdown()
