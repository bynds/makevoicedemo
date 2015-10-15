# Required to support the network configuration file
from configuration import Configuration

# Used for printing the Hue exception
import sys

# Coroutine concurrency (http://sdiehl.github.io/gevent-tutorial/#core) imports
import grequests
import gevent

# This method is used as a callback for the asynchronous network communications used to speak to the hub.
# Our version is very simplistic and just outputs the HTTP Response Code to the console.


def printStatus(response, **kwargs):
    print "Hue response was {}".format(response.status_code)

# The following allows us to specify the IP address and username in a more friendly JSON configuration file rather than 
# hardcoding the values in the Python source.

configuration = Configuration()
config = configuration.loadConfig()
hub = config['hue']


class Hue():
    def turn(self, deviceId='', onOrOff=''):
        if onOrOff == 'on':
            self.turnLightOn(deviceId)
        if onOrOff == 'off':
            self.turnLightOff(deviceId)

    def turnLightOn(self, deviceId):
        # The grequests library sends the request as soon as we create "job" below. We then yield to the greenlet every hundredth of a second
        # in the main update method to ensure we capture the result.
        req = grequests.put(
            'http://{ip}/api/{username}/lights/{devId}/state'.format(
                ip=hub['IP'],
                username=hub['username'],
                devId=deviceId),
            callback=printStatus,
            data='{"on":true,"bri":254}',
            timeout=4)
        job = grequests.send(req, grequests.Pool(1))
        job.link_exception(lambda *kwargs: sys.stdout.write(
            "There was an exception with the Hue request"))

    def turnLightOff(self, deviceId):
        # The grequests library sends the request as soon as we create "job" below. We then yield to the greenlet every hundredth of a second
        # in the main update method to ensure we capture the result.
        req = grequests.put(
            'http://{ip}/api/{username}/lights/{devId}/state'.format(
                ip=hub['IP'],
                username=hub['username'],
                devId=deviceId),
            callback=printStatus,
            data='{"on":false}',
            timeout=4)
        job = grequests.send(req, grequests.Pool(1))
        job.link_exception(lambda *kwargs: sys.stdout.write(
            "There was an exception with the Hue request"))
