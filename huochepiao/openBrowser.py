# from splinter.browser import Browser
#
# driver_name = 'chrome'
# executable_path = '/usr/local/bin/chromedriver'
# driver = Browser(driver_name=driver_name, executable_path=executable_path)


from selenium import webdriver

driver = webdriver.Chrome()
base_url = 'https://www.baidu.com'
driver.get(base_url)


# from selenium import webdriver
#
# path = "./chromedriver" # chromedriver完整路径，path是重点
# driver = webdriver.Chrome(path)
# base_url = 'https://www.baidu.com'
# driver.get(base_url)


