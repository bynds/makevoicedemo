# This is required to be able to "Monkey Patch"  (https://www.google.com/search?q=define:monkey+patch) a number of 
# modules in the Python standard library to make them cooperative. This gives us an easy way to play with the idea
# of asynchronous programming.
import gevent

# The following import will allow us to view exceptions with a good level of detail in the case of something unexpected.
import sys, traceback

# The configuration class is what we will use to read from our special configuartion file.
from configuration import Configuration

# The following two files are imported to let us speak to the Insteon and Philips Hue hubs. We speak to these hubs
# using the same standard HTTP protocol that allows you to view web pages on the Internet.
from hue import Hue
from insteon import Insteon

# The following file is imported so that we can send commands to our Arduino which will then be translated into 
# IR control commands to be sent to the Roomba
from roomba import Roomba

# This import will give us our wrapper for the Pocketsphinx library which we can use to get the voice commands from the 
# user.
from pocket_sphinx_listener import PocketSphinxListener

gevent.monkey.patch_all()


def runMain():
    # First, we import our devices from our configuration file. These will be split into two different groups, those
    # controlled by Philips Hue and those controlled by Insteon.
    configuration = Configuration()
    config = configuration.loadConfig()

    hueDevices = {}
    insteonDevices = {}

    for device in config['devices']['hue']:
        hueDevices[device] = config['devices']['hue'][device]
    for device in config['devices']['insteon']:
        insteonDevices[device] = config['devices']['insteon'][device]
    insteon = Insteon()
    hue = Hue()

    roomba = Roomba()

    # Now we set up the voice recognition using Pocketsphinx from CMU Sphinx.
    pocketSphinxListener = PocketSphinxListener()

    # We want to run forever, or until the user presses control-c, whichever comes first.
    while True:
        try:
            command = pocketSphinxListener.getCommand().lower()
            command = command.replace('the', '')

            if command.startswith('turn'):
                onOrOff = command.split()[1]
                deviceName = ''.join(command.split()[2:])
                if deviceName in hueDevices:
                    deviceId = hueDevices[deviceName]['deviceID']
                    hue.turn(deviceId=deviceId, onOrOff=onOrOff)
                if deviceName in insteonDevices:
                    deviceId = insteonDevices[deviceName]['deviceID']
                    insteon.turn(deviceId=deviceId, onOrOff=onOrOff)
                if deviceName == 'roomba':
                    roomba.turn(onOrOff)
            elif command.startswith('roomba'):
                action = ' '.join(command.split()[1:])
                if action == 'clean':
                    roomba.clean()
                if action == 'go home':
                    roomba.goHome()

        # This will allow us to be good cooperators and sleep for a second.
        # This will give the other greenlets which we have created for talking 
        # to the Hue and Insteon hubs a chance to run.
            gevent.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            print 'People sometimes make mistakes, Goodbye.'
            sys.exit()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2,
                                      file=sys.stdout)
            sys.exit()


if __name__ == '__main__':
    runMain()
