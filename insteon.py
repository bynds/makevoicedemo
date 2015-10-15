# This is used to encode the username and password for the HTTP Header
import base64

# Required to support the network configuration file
from configuration import Configuration

# Used for printing the Insteon exception
import sys

# Coroutine concurrency (http://sdiehl.github.io/gevent-tutorial/#core) imports
import grequests
import gevent

# This method is used as a callback for the asynchronous network communications used to speak to the hub.
# Our version is very simplistic and just outputs the HTTP Response Code to the console.


def printStatus(response, **kwargs):
    print "Insteon response was {}".format(response.status_code)

# The following allows us to specify the IP address, username and password in a more friendly JSON configuration file rather than 
# hardcoding the values in the Python source.

configuration = Configuration()
config = configuration.loadConfig()
hub = config['insteon']


class Insteon():
    def turn(self, deviceId='', onOrOff=''):
        if onOrOff == 'on':
            self.turnLightOn(deviceId)
        if onOrOff == 'off':
            self.turnLightOff(deviceId)

    def turnLightOn(self, deviceId):
        # The grequests library sends the request as soon as we create "job" below. We then yield to the greenlet every hundredth of a second
        # in the main update method to ensure we capture the result.
        base64string = base64.encodestring(
            '%s:%s' % (hub['username'], hub['password'])).replace('\n', '')
        req = grequests.get(
            'http://{ip}/3?0262{devId}0F11FF=I=3'.format(ip=hub['IP'],
                                                         devId=deviceId),
            callback=printStatus,
            timeout=4,
            headers={"Authorization": "Basic %s" % base64string})
        job = grequests.send(req, grequests.Pool(1))
        job.link_exception(lambda *kwargs: sys.stdout.write(
            "There was an exception with the Insteon request"))

    def turnLightOff(self, deviceId):
        # The grequests library sends the request as soon as we create "job" below. We then yield to the greenlet every hundredth of a second
        # in the main update method to ensure we capture the result.
        base64string = base64.encodestring(
            '%s:%s' % (hub['username'], hub['password'])).replace('\n', '')
        req = grequests.get(
            'http://{ip}/3?0262{devId}0F13FF=I=3'.format(ip=hub['IP'],
                                                         devId=deviceId),
            callback=printStatus,
            timeout=4,
            headers={"Authorization": "Basic %s" % base64string})
        job = grequests.send(req, grequests.Pool(1))
        job.link_exception(lambda *kwargs: sys.stdout.write(
            "There was an exception with the Insteon request"))
