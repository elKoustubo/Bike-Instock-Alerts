import os, logging, requests
from logging import handlers
from bs4 import BeautifulSoup
from datetime import date

#Setting up logger
rfh = handlers.RotatingFileHandler(
    filename='alert.log', 
    mode='a',
    maxBytes=10*1024, # Limiting log size to 10kbs
    backupCount=1)
logging.basicConfig(#filename='alert.log', filemode='a',
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d',
    handlers=[rfh])
logger=logging.getLogger() 
# List of our desired bikes
with open('bike_urls.txt') as bikes:
    bikes = bikes.readlines()
# Function to get url of our desired bike and in its desired size
# Please note that url must point to a specific bike and size for our getalert function to work correctly
def geturl(opbike:int=1, opsize:str='S'): # My bike size is S, hence it's default
    mainurl = bikes[opbike].strip('\n')
    # Each bike has a unique 4 digit identifier, we will extract that from mainurl
    bikecode = mainurl.split('/')[9][:4]
    #When bike is available for size selection, then we will need to append the size portion of url string to main url
    sizeurl = "&dwvar_"+bikecode+"_pv_rahmengroesse="

    return mainurl+sizeurl+opsize

# Alert if the item is available to be added to cart i.e. it is in stock, yay!
def getalert(url = geturl()):
    alert = False # Default 
    bike = url.split('/')[8] # Bike name
    try:
        page = requests.get(url)
    except:
        print("Failed to connect!!!")
        
    # Status Code = 200 indicates "everything went as expected"
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser') # Parse page contents
        # If the item is in stock then "Add to cart" button is available. Using BS4 to find desired "button" class
        to_cart = soup.findAll("button", {"class":"button js-addToCart-button productDescription__addToCart js-chooseVariation button--primary"})
        alert = (len(to_cart) != 0) # True if "Add to cart" button exists
        return alert, bike

# Using Twilio free account to send myself SMS if the desired item is in stock!
def checkstock(opbike:int=1, opsize:str='S'):
    alert, bike = getalert(geturl(opbike,opsize))

    # First check if an Alert was sent on that particular day, I do not wish to spam my inbox
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    
    with open('alert.log') as f:
        f = f.readlines() # Let's review our logs

    for line in f:
        if bike in line: # If log has entry for today then alert was already sent
            if today in line: 
                alert = False
                break
        
    if alert:
        from twilio.rest import Client

        # Initiate Twilio client
        def setup_twilio_client():
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            return Client(account_sid, auth_token)

        # Define SMS content, sender, receiver  
        def send_notification():
            twilio_client = setup_twilio_client()
            twilio_client.messages.create(
                body="Your " + bike + " is available for purchase.",
                from_=os.getenv('TWILIO_FROM_NUMBER'),
                to=os.getenv('MY_PHONE_NUMBER')
            )
        setup_twilio_client()
        send_notification()
        logger.info(f'Alert for {bike} was sent!')

# Get alerted if any of the bike in our shortlist comes back in stock!!! Hurrah!
for i in range(len(bikes)-1):
    checkstock(opbike=i+1)

#checkstock(opbike=0,opsize='2XL')  # Uncomment for SMS Alert Test 

