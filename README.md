# Stock-Market-Simulation

The Stock Market is extremely complex and dependent on many factors, making it very stressful to keep up with everything. So, what if it is dumbed down to randomly buying and selling stocks? How would this compare to common indices such as the S&P500 and NASDAQ? These are what this project aim to answer.

At given periods throughout trading hours, a random stock is chosen from the S&P500 and a random amount is either bought or sold. To create randomness, I didn't want to use Python's "random" library because it's not really random (though nothing really is), so I opted to utilize my own method of generating a random value between two values a,b where a < b:

$\frac{b-a}{2} * sin(UnitedStatesDebt * CME) + \frac{b+a}{2}$

where CME is the [number of things that will get hit by our Sun's Coronal Mass Ejections that day.](https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?startDate=2023-10-09&endDate=2023-10-09)

In using this Random Number Generator (RNG), it doesn't make much since for it to create negative number because I can't buy a negative number of stocks. So, a = 0 thus producing the equation 

$\frac{b}{2} * sin(UnitedStatesDebt * CME) + \frac{b}{2}$

where b is the maximum value I want to generate

If the U.S. debt (taken from [this website](https://www.usdebtclock.org/world-debt-clock.html)) is even, then I wish to buy. Of the 500 stocks in the S&P500, I need to choose one to buy. So, I generate a value between 0 and 500 using the equation above and I buy the stock that is at that location in the list of S&P500 companies. So, if the equation spits out 300, then I buy the 300th stock in the list of S&P500 companies. Then, I use the equation again to generate the amount of stocks I can buy, with the max amount being 100 shares.

If the U.S. debt is odd, I randomly select a share from the current portfolio using the equation above and randomly choose an amount to sell, updating my portfolio value and profit accordingly. 

I am in the process of adding features that quantify its performance such as beta, sharpe ratio, how well the protfolio handles major market-moving events, etc.

This is run on an AWS EC2 instance.

