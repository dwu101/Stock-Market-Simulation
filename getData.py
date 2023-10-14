import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from settings import RapidAPIHeader


def getDebt():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get("https://www.usdebtclock.org/world-debt-clock.html")

    element = driver.find_element_by_id("layer3")
    USdebt = int(element.text.replace(',', '')[1:])

    driver.quit()

    return USdebt


def getCME(date): #date format yyyy-mm-dd
    nasaURL = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CME?startDate={x}&endDate={x}'.format(x=date)

    try:
        response = requests.get(nasaURL) #sometimes this doesn't return anything

        if response.status_code == 200:
            data = response.json()

            if not data:
                return -1
            
            totalImpacts = 0
            for item in data:
                for singleAnalysis in item['cmeAnalyses']:
                    if singleAnalysis['enlilList']:
                        for enlilList in singleAnalysis['enlilList']: #sometimes singleAnalysis['enlilList] == null
                            totalImpacts += len(enlilList['impactList'])  
                    
            return totalImpacts


        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return -1

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return -1


def getStockPrice(ticker): #https://rapidapi.com/sparior/api/yahoo-finance15/

    try:

        url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{x}/financial-data".format(x=ticker)

        headers = RapidAPIHeader

        response = requests.get(url, headers=headers)

        return response.json()['financialData']['currentPrice']['raw'] 
    
    except:
        return 0

def main():
    print(getCME('2023-10-03'))
    print(getDebt())
    print(getStockPrice("AAPL"))

main()