import sys
import json
import cbpro
import time
from datetime import datetime

now = datetime.now()
key = 'XXXXXXXXXXXXXXX'  #Coinbase Pro API Key
b64secret = 'XXXXXXXXXXXXXXX' #Coinebase Pro API b64secret
passphrase = 'XXXXXXXXXXXXX' #Coinabase Pro API passphrase
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

def checkWallet(accountType):
    #Check wallet and return BTC or USD balances

    usdAcctID = '16ed818c-3a69-4642-9f2e-ecf5cf4c1087'
    btcAcctID = '651cca3c-2f1a-463f-b174-f92923fcfd64'
    if accountType == 'usd':
        accountID = usdAcctID
    elif accountType == 'btc':
        accountID = btcAcctID

    accountBalance = auth_client.get_account(accountID)
    accountBalanceStripped = json.loads(json.dumps(accountBalance))
    return(accountBalanceStripped['available'])


def currentPrice():
    #Check stock and return BTC price

    price = auth_client.get_product_ticker(product_id='BTC-USD')
    btcPrice = json.loads(json.dumps(price))
    cbtcPrice = float(btcPrice['bid'])
    return(cbtcPrice)


def prices():
    try:

        while True:
            if currentPrice() <= 5800:
                cbtcPrice = currentPrice()
                buy(cbtcPrice)
            else:
                print(currentPrice())
                time.sleep(5)
    except KeyboardInterrupt:
        print "\nQuitting...."


def buy(boughtPrice):
    if checkWallet('usd') > 500:
        bought = 500
        auth_client.buy(price='503.00', size='0.01', order_type='limit', product_id='BTC-USD') #0.01=BTC
        currentDate = dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print "Bought BTC with ${} when price was {}".format(bought, boughtPrice)
        f = open("logs.txt", "a+")
        f.write ("Bought BTC with ${} when price was {} on {} ".format(bought, boughtPrice, currentDate)+"\n")
        sell(bought, boughtPrice)
    else:
        print("Insufficient funds")
        time.sleep(5)
        prices()


def equation(x, y):

    percentage = 60 / float(x)
    goal = y + (y * percentage)
    return (goal)


def sell(bought, boughtPrice):
    try:
        while True:
     
            if currentPrice() >= equation(bought, boughtPrice):
                auth_client.sell(price='500.00', size='0.01', order_type='limit', product_id='BTC-USD')
                print("Sold on {}").format(currentPrice())
                f = open("logs.txt", "a+")
                f.write ("Bought BTC with ${} when price was {} on {} ".format(bought, boughtPrice, currentDate)+"\n")
                quit()
            else:
                print(currentPrice())
                time.sleep(5)
    except KeyboardInterrupt:
        print "\nQuitting...."

def main():
    prices()

main()
