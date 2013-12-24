import logging

import config
import subprocess
from PageEvents.clEvents import CLEvents
import CL_AutoFlagging
import copy

module_logger = logging.getLogger('main.FlagAllAds')


def flagAllAds():
    config.finalProxies = []
    #============= Loop through all ads =============
    for currentAd in config.ads:
        if currentAd.adStatus is 'FLAGGED':
            continue

        for x in xrange(len(config.proxies) * 3):
            setupFinalProxies()
            print len(config.finalProxies)
            currentProxy = config.finalProxies.pop(0)

            #========== Setup Firefox with proxy ============
            cle = CLEvents(currentProxy)
            # noinspection PyBroadException
            try:
                subprocess.Popen(
                    CL_AutoFlagging.get_main_dir() + "/Resources/Proxy_Auth.exe " + currentProxy.ProxyUsername + " " + currentProxy.ProxyPassword)
                cle.navigate(currentAd.adURL)
                if cle.checkIfAdFlagged():
                    currentAd.adStatus = 'FLAGGED'
                else:
                    cle.flagCurrentAd()
                    if cle.checkIfAdFlagged():
                        currentAd.adStatus = 'FLAGGED'
            except:
                raise
            if currentAd.adStatus == 'FLAGGED':
                adLink = currentAd.adURL[currentAd.adURL.rfind('/') + 1:currentAd.adURL.rfind('.')]
                fileName = adLink + ".png"
                currentAd.imagePath = config.outputImagesPath + fileName
                cle.takeScreenshot(currentAd.imagePath)

            cle.destroy()

            if currentAd.adStatus == 'FLAGGED':
                break


def setupFinalProxies():
    if len(config.finalProxies) == 0:
        config.finalProxies = copy.deepcopy(config.proxies)
    else:
        return

