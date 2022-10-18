from selenium import webdriver
browser = webdriver.Firefox(executable_path="/Users/luciepellier/Documents/Projects/CryptoApp/cryptos/geckodriver")
browser.get('http://google.com/')
print(browser.title)


