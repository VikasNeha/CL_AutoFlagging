import logging

from xlrd import open_workbook
from xlwt import easyxf, Formula, Workbook

import config


module_logger = logging.getLogger('main.inputContent')
inputFile = config.inputXLSPath
outputFile = config.outputXLSPath


class Proxy:
    ProxyAddress = None
    ProxyPort = None
    ProxyUsername = None
    ProxyPassword = None


class Ads:
    adURL = None
    adStatus = None
    imagePath = None
    row = None


def readProxies():
    module_logger.info("Reading Proxies")
    book = open_workbook(config.inputXLSPath)
    sheet = book.sheet_by_name('Proxies')
    config.proxies = []
    for row in range(sheet.nrows):
        if row == 0:
            continue
        tempProxy = Proxy()
        for col in range(sheet.ncols):
            if col == 0:
                tempProxy.ProxyAddress = sheet.cell(row, col).value
            elif col == 1:
                tempProxy.ProxyPort = str(int(sheet.cell(row, col).value))
            elif col == 2:
                tempProxy.ProxyUsername = sheet.cell(row, col).value
            elif col == 3:
                tempProxy.ProxyPassword = sheet.cell(row, col).value
        config.proxies.append(tempProxy)


def readAds():
    module_logger.info("Reading Ads")
    book = open_workbook(config.inputXLSPath)
    sheet = book.sheet_by_name('Ads')
    config.ads = []
    for row in range(sheet.nrows):
        if row == 0:
            continue
        tempAd = Ads()
        tempAd.row = row
        for col in range(sheet.ncols):
            if col == 0:
                tempAd.adURL = sheet.cell(row, col).value
        config.ads.append(tempAd)


def writeResults():
    module_logger.info("Writing Results")
    wb = Workbook()
    ws = wb.add_sheet(sheetname='Ads Results')
    headerStyle = easyxf('font: bold True')
    ws.write(0, 0, "Ad URLs", headerStyle)
    ws.write(0, 1, "Ad Status", headerStyle)
    ws.write(0, 2, "Image Path", headerStyle)

    hyperlinkStyle = easyxf('font: underline single, colour dark_blue')

    max_width_col0 = 0
    max_width_col1 = 0
    max_width_col2 = 0
    for currentAd in config.ads:
        ws.write(currentAd.row, 0, currentAd.adURL)
        if max_width_col0 < len(currentAd.adURL):
            max_width_col0 = len(currentAd.adURL)
        if currentAd.adStatus is not None:
            ws.write(currentAd.row, 1, currentAd.adStatus)
            if max_width_col1 < len(currentAd.adStatus):
                max_width_col1 = len(currentAd.adStatus)
        if currentAd.imagePath is not None:
            link = 'HYPERLINK("' + currentAd.imagePath + '";"' + currentAd.imagePath + '")'
            ws.write(currentAd.row, 2, Formula(link), hyperlinkStyle)
            if max_width_col2 < len(currentAd.imagePath):
                max_width_col2 = len(currentAd.imagePath)

    ws.col(0).width = 256 * max_width_col0
    ws.col(1).width = 256 * (max_width_col1+5)
    ws.col(2).width = 256 * max_width_col2

    wb.save(config.outputXLSPath)