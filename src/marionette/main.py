import os
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

    # Click to activate start page
    tabs: list[HTMLElement] = marionette.find_elements('class name', 'tabmail-tab')
    tabs[0].click()

    # Wait until start page is loaded-ish
    time.sleep(2)

    # Dump screenshot into out.png
    with open('./mail-screen.png', 'wb') as fh:
        marionette.save_screenshot(fh)

    calendar_btn: HTMLElement = marionette.find_element('id', 'calendarButton')
    calendar_btn.click()

    time.sleep(1)

    # Dump screenshot into out.png
    with open('./calendar-screen.png', 'wb') as fh:
        marionette.save_screenshot(fh)

    marionette.delete_session()


if __name__ == "__main__":
    print("Running Marionette...")
    run()
    print("Done!")

