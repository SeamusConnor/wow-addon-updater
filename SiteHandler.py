import packages.requests as requests


# Site splitter

def findZiploc(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return curse('https://www.curseforge.com/wow/addons/' + addonpage.split('/')[-1])
    elif addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return curse(addonpage)

    # Tukui
    elif addonpage.startswith('http://git.tukui.org/'):
        return tukui(addonpage)

    # Wowinterface
    elif addonpage.startswith('http://www.wowinterface.com/'):
        return wowinterface(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


def getCurrentVersion(addonpage):
    # Curse
    if addonpage.startswith('https://mods.curse.com/addons/wow/'):
        return getCurseVersion('https://www.curseforge.com/wow/addons/' + addonpage.split('/')[-1])
    elif addonpage.startswith('https://www.curseforge.com/wow/addons/'):
        return getCurseVersion(addonpage)

    # Tukui
    elif addonpage.startswith('http://git.tukui.org/'):
        return getTukuiVersion(addonpage)

    # Wowinterface
    elif addonpage.startswith('http://www.wowinterface.com/'):
        return getWowinterfaceVersion(addonpage)

    # Invalid page
    else:
        print('Invalid addon page.')


# Curse

def curse(addonpage):
    try:
        page = requests.get(addonpage + '/download')
        contentString = str(page.content)
        indexOfZiploc = contentString.find('download__link') + 22  # Will be the index of the first char of the url
        endQuote = contentString.find('"', indexOfZiploc)  # Will be the index of the ending quote after the url
        return 'https://www.curseforge.com' + contentString[indexOfZiploc:endQuote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def getCurseVersion(addonpage):
    try:
        page = requests.get(addonpage + '/files')
        contentString = str(page.content)
        indexOfVer = contentString.find('file__name full') + 17  # first char of the version string
        endTag = contentString.find('</span>', indexOfVer)  # ending tag after the version string
        return contentString[indexOfVer:endTag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''


# Tukui

def tukui(addonpage):
    print('Tukui is not supported yet.')
    return ''


def getTukuiVersion(addonpage):
    # print('Tukui is not supported yet.')
    return ''


# Wowinterface

def wowinterface(addonpage):
    downloadpage = addonpage.replace('info', 'download')
    try:
        page = requests.get(downloadpage + '/download')
        contentString = str(page.content)
        indexOfZiploc = contentString.find('Problems with the download? <a href="') + 37  # first char of the url
        endQuote = contentString.find('"', indexOfZiploc)  # ending quote after the url
        return contentString[indexOfZiploc:endQuote]
    except Exception:
        print('Failed to find downloadable zip file for addon. Skipping...\n')
        return ''


def getWowinterfaceVersion(addonpage):
    try:
        page = requests.get(addonpage)
        contentString = str(page.content)
        indexOfVer = contentString.find('id="version"') + 22  # first char of the version string
        endTag = contentString.find('</div>', indexOfVer)  # ending tag after the version string
        return contentString[indexOfVer:endTag].strip()
    except Exception:
        print('Failed to find version number for: ' + addonpage)
        return ''
