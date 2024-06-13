from marionette_driver.marionette import Marionette, ActionSequence

client = Marionette('127.0.0.1', port=2828)
client.start_session()

client.set_context(client.CONTEXT_CHROME)

# Dump screenshot into out.png
with open('./out.png', 'wb') as fh:
    client.save_screenshot(fh)

print("Done!")