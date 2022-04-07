import requests
from bs4 import BeautifulSoup


def geturl(opbike:int=1, optype:int=1, opsize:str='S'): # My bike size is S, hence it's default
    if opbike == 1: #Endurace family
        mainurl = "https://www.canyon.com/en-us/road-bikes/endurance-bikes/endurace/"
        if optype == 1: # endurace-cf-sl-7-disc
            opt = "cf-sl/endurace-cf-sl-7-disc/2962.html?dwvar_2962_pv_rahmenfarbe=YE%2FBK&dwvar_2962_pv_rahmengroesse=" + opsize
        elif optype == 2: # BLUE endurace-8-disc
            opt = "al/endurace-8-disc/2854.html?dwvar_2854_pv_rahmenfarbe=BK%2FBU&dwvar_2854_pv_rahmengroesse=" + opsize
        elif optype == 3: # BLACK endurace-8-disc
            opt = "al/endurace-8-disc/2854.html?dwvar_2854_pv_rahmenfarbe=BK%2FBK&dwvar_2854_pv_rahmengroesse=" + opsize
    elif opbike == 2: # 
        mainurl = "https://www.canyon.com/en-us/gravel-bikes/bike-packing/grizl/"
        if optype == 1: # grizl-cf-sl-6
            opt = "cf-sl/grizl-cf-sl-6/3243.html?dwvar_3243_pv_rahmenfarbe=YE&dwvar_3243_pv_rahmengroesse=" + opsize
        elif optype == 2: # grizl-7
            opt = "al/grizl-7/2845.html?dwvar_2845_pv_rahmenfarbe=GY%2FBK&dwvar_2845_pv_rahmengroesse=" + opsize
    elif opbike == 3: # This is an option to test code for a bike that we know is in stock
        mainurl = "https://www.canyon.com/en-us/road-bikes/endurance-bikes/endurace/"
        opt = "cf-sl/endurace-cf-sl-8-disc-di2/3384.html?dwvar_3384_pv_rahmenfarbe=GY%2FBK&dwvar_3384_pv_rahmengroesse=XL"

    return mainurl+opt


def getalert(url = geturl()):
    bike = url.split('/')[8] # Bike name
    try:
        page = requests.get(url)
    except:
        page.status_code = 0
        

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        to_cart = soup.findAll("button", {"class":"button js-addToCart-button productDescription__addToCart js-chooseVariation button--primary"})
        alert = (len(to_cart) != 0)
        return alert, bike

def checkstock(opbike:int=1, optype:int=1, opsize:str='S'):
    alert, bike = getalert(geturl(opbike,optype,opsize))

    if alert:
        import killi
        from twilio.rest import Client
        def setup_twilio_client():
            account_sid = killi.TWILIO_ACCOUNT_SID()
            auth_token = killi.TWILIO_AUTH_TOKEN()
            return Client(account_sid, auth_token)

        def send_notification():
            twilio_client = setup_twilio_client()
            twilio_client.messages.create(
                body="Your " + bike + " is available for purchase.",
                from_=killi.TWILIO_FROM_NUMBER(),
                to=killi.MY_PHONE_NUMBER()
            )
        setup_twilio_client()
        send_notification()

# Get alerted if any of the following bike comes back in stock!!! Hurrah!
checkstock(optype=1)
checkstock(optype=2)
checkstock(optype=3)
checkstock(opbike=2, optype=1)
checkstock(opbike=2, optype=2)

# checkstock(opbike=3)  # Uncomment for SMS Alert Test

