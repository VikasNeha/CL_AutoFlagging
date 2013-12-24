from selenium.common.exceptions import TimeoutException
from webpageEvents import WebpageEvents
from Utilities.constants import IDMODE


class CLEvents(WebpageEvents):
    def __init__(self, currentProxy):
        super(CLEvents, self).__init__(currentProxy)

    def destroy(self):
        super(CLEvents, self).destroy()

    def checkIfAdFlagged(self):
        try:
            if self.findElement(IDMODE.CLASS, 'flagChooser'):
                return False
        except TimeoutException:
            try:
                if 'This posting has been flagged for removal' in self.getElementText(IDMODE.CLASS, 'removed'):
                    return True
                else:
                    return False
            except TimeoutException:
                return False

    def flagCurrentAd(self):
        try:
            self.clickPartialLink('spam')
        except:
            raise