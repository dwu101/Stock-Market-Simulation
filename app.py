from getData import getStockPrice, getCME, getDebt
from NASDAQstocks import allStocks #11540 long
import time
import numpy as np
import math
from datetime import datetime


def RandomFromDebt(debt, upperBound):
    coeff = upperBound//2
    randomVal = math.floor(coeff*np.sin(debt) + coeff)

    return randomVal

def updatePortfoio(portfolio, stock, amtBought):
    if amtBought:
        if stock in portfolio:
            portfolio[stock] += amtBought 
        else:
            portfolio[stock] = amtBought


def main():
    portfolio = {}
    budget = 1000000
    portfolioValue = 0
    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")

    while True:
        print(portfolio, portfolioValue)
        debt = getDebt()
        isOdd = debt % 2
        cme =getCME(formatted_date) + 1 #in case its 0

        if not isOdd: #BUY BABY BUY
            print('x')
            stock = RandomFromDebt(debt*cme, 11539) #gets random stock
            stockPrice = getStockPrice(allStocks[stock]) 

            while not stockPrice: #in case the randomly generated stock is unavabile in the api
                print("trying again...")
                debt*=cme
                stock = RandomFromDebt(debt, 11539)
                stockPrice = getStockPrice(allStocks[stock]) 

            maxCanBuy = budget // stockPrice

            if maxCanBuy:
                maxCanBuy = min(maxCanBuy,500) #if maxCanBuy is 0, do nothing and all the lines under will effectly do nothing. else, cap it at 500 for diversification
            
            debt = getDebt()#get a new debt for more randomness for the below code

            amt = RandomFromDebt(debt, maxCanBuy) #generates a random amount of stock that can be bought

            budget -= amt*stockPrice #wat do when budget = 0 or is very close to 0
            portfolioValue += amt*stockPrice

            updatePortfoio(portfolio, allStocks[stock], amt)   
        else:
            print("y")



        


main()