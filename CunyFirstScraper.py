import requests
from lxml import html
import sql

def getCredentials(accountID):
    # needs to access database record of accountID and pull username into credentials[0], and password into credentials[1]
    credentials = ['David.Belinsky58', 'Roy13dvb^']
    return credentials

def scrapeCFirst(accountID):
    credentials = sql.getCredentials(accountID)
    session_requests = requests.session()
    login_url = "https://home.cunyfirst.cuny.edu/access/dummy.cgi"
    payload = {"login": "Username", "password": "Password"}
    payload["login"] = credentials[0]
    payload["password"] = credentials[1]
    result = session_requests.post(login_url, data = payload, headers = dict(referer = login_url))
    url = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"
    result = session_requests.get(url, headers = dict(referer = url))
    tree = html.fromstring(result.content)
    stuff = tree.xpath("//td[@class='PSLEVEL3GRID']/div/span/text()")
    classes = []
    classi = []
    for a in stuff:
        classi.append(a)
        if len(classi) == 4:
            classes.append(classi)
            classi = []
    return classes
