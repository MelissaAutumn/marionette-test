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
    marionette.restart()

    marionette.set_window_rect(0, 0, 768, 1360)

    time.sleep(1)

    # Click to activate start page
    tabs: list[HTMLElement] = marionette.find_elements('class name', 'tabmail-tab')
    tabs[0].click()

    # This script sets some things unread, as tagged, and unhides the attachment icon. It then selects the main email.
    marionette.execute_script("""
    // Grab the list of messages
    const tree = document.querySelectorAll('browser')[1].browsingContext.window.threadPane.treeTable.parentElement;
    let messages = document.querySelectorAll('browser')[1].browsingContext.window.threadPane.treeTable.querySelectorAll('.card-layout');
    const main = messages[1];
    const expanded = messages[3];
    const unread = [messages[6], messages[10]];
    const attachments = [messages[0], messages[1], messages[2], messages[3], messages[4], messages[8]];
    const tagged = {
        1: ['cmd_tag1', 'cmd_tag2', 'cmd_tag4', 'cmd_tag6', 'cmd_tag7'],
        2: ['cmd_tag5', 'cmd_tag6'],
        5: ['cmd_tag3', 'cmd_tag7'],
        8: ['cmd_tag6', 'cmd_tag7'],
        9: ['cmd_tag2', 'cmd_tag5'],
    };
    
    // Expand the expanded!
    expanded.querySelector('.thread-card-last-row > button').click()
    
    // We've expanded an email, so refresh the emails here!
    messages = document.querySelectorAll('browser')[1].browsingContext.window.threadPane.treeTable.querySelectorAll('.card-layout');
    
    // Un-new everything!!
    messages.forEach((el) => el.dataset['properties'].replace('new', ''));
    
    const newMsg = messages[5];

    // Tag some mail
    Object.entries(tagged).forEach((tuple) => {
        const el = messages[tuple[0]];
        const cmds = tuple[1];
        
        // Select
        el.click();
        cmds.forEach((cmd) => goDoCommand(cmd));
    }); 
    
    // Show some attachment icons
    attachments.forEach((el) => { el.querySelector('.thread-card-icon-info > .attachment-icon').style.display = 'block'; });
    
    // Set the unread mails
    unread.forEach((el) => { el.dataset['properties'] = 'unread offline'; });

    // Set it as new    
    newMsg.dataset['properties'] = 'unread new offline thread-children';

    // And finally, show the beautiful email!
    messages[1].click();
    tree.scrollTo(0,0);
    """)

    time.sleep(5)

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
