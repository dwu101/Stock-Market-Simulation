from getData import getStockPrice, getCME, getDebt
from companies import allStocks #len = 505
import time
import numpy as np
import math
from datetime import datetime


def RandomFromDebt(debt, upperBound):
    coeff = upperBound//2
    randomVal = math.floor(coeff*np.sin(debt) + coeff)

    return randomVal

def updatePortfolio(portfolio,portfolioBuyHistory, stock, amtBought, priceBought):
    if amtBought:
        if stock in portfolio:
            portfolio[stock] += amtBought 
        else:
            portfolio[stock] = amtBought
    
        if stock in portfolioBuyHistory:
            portfolioBuyHistory[stock].append([priceBought, amtBought])
        else:
            portfolioBuyHistory[stock] = [[priceBought, amtBought]]

def main():

    portfolio = {} # {ticker: amount}
    portfolioBuyHistory = {} #{ticker: [ [price, amount]]}. I will uses FIFO method when selling.
    profit = 0 
    budget = 50000
    portfolioValue = 0

    

    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")

    while True:
        
        
        debt = getDebt()
        isOdd = debt % 2
        cme =getCME(formatted_date) + 1 #in case its 0

        print("portfolio", portfolio,"\n",
           "portoflioBuyHistory",portfolioBuyHistory,"\n",
           "profit", profit, "\n",
           "budget", budget, "\n",
           "portfolioValue",portfolioValue,"\n",
           "debt", debt,"\n",
           "cme", cme,"\n")

        if not isOdd: #BUY BABY BUY
            print('x')
            stock = RandomFromDebt(debt*cme, 504) #gets random stock
            ticker = allStocks[stock]['Symbol']
            currStockPrice = getStockPrice(ticker) 

            correction = 0 #if cme is odd and debt is odd, then product will always be odd, creating infinite loop.

            while not currStockPrice: #in case the randomly generated stock is unavabile in the api
                print("trying again...")
                debt*= (cme + correction)
                stock = RandomFromDebt(debt, 504)
                currStockPrice = getStockPrice(ticker) 
                correction += 1

            maxCanBuy = budget // currStockPrice

            if maxCanBuy:
                maxCanBuy = min(maxCanBuy,100) #if maxCanBuy is 0, do nothing and all the lines under will effectly do nothing. else, cap it at 500 for diversification
            
            debt = getDebt()#get a new debt for more randomness for the below code

            amt = RandomFromDebt(debt, maxCanBuy) #generates a random amount of stock that can be bought

            budget -= amt*currStockPrice #wat do when budget = 0 or is very close to 0
            portfolioValue += amt*currStockPrice

            updatePortfolio(portfolio, portfolioBuyHistory, ticker, amt, currStockPrice)   


        else: #SELL
            print("y")
            if portfolio: #do nothing if portfolio is empty 
                stockInPortfolio = RandomFromDebt(debt*cme, len(portfolio)-1) #gets a random stock from the portfolio
                ticker = list(portfolio.items())[stockInPortfolio][0]
                amtHolding = portfolio[ticker]

                amtToSell = math.floor(RandomFromDebt(debt*cme, amtHolding)) #gets how many to sell

                portfolio[ticker] -= amtToSell #adjusts portfolio

                currStockPrice = getStockPrice(ticker) 

                counter = 0 

                pricetoConsider = portfolioBuyHistory[ticker][0][0]
                amtToConsider = portfolioBuyHistory[ticker][0][1]

                while counter + amtToConsider <= amtToSell: #index 0 gives the first stock price
                    profit += (currStockPrice - pricetoConsider) * amtToConsider
                    portfolioValue -= pricetoConsider *amtToConsider
                    budget += pricetoConsider*amtToConsider
                        
                    portfolioBuyHistory[ticker].pop(0)
                    counter += amtToConsider

                    pricetoConsider = portfolioBuyHistory[ticker][0][0]
                    amtToConsider = portfolioBuyHistory[ticker][0][1] 
                
                if counter != amtToSell: #this means that I should only sell part of portfolioBuyHistory[ticker][0]
                    difference = amtToSell - counter #how many more i need to sell

                    profit += (currStockPrice - pricetoConsider) * difference
                    portfolioValue -= pricetoConsider *difference
                    budget += pricetoConsider* difference

                    portfolioBuyHistory[ticker][0][1] -= difference

                    

                        

                        

                

        


main()