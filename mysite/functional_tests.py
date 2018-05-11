''' functional tests for the menu app
'''
from selenium import webdriver

        
browser = webdriver.Firefox()
browser.get('http://www.facebook.com')

assert 'Facebook' in browser.title