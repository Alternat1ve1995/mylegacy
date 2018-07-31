from selenium import webdriver
import subprocess
from time import sleep


def start(login, password, url, delay=10):
	browser = webdriver.Chrome('./chromedriver.exe')
	try: browser.get(url)
	except:
		print '\n[ERROR] Invalid url address.'
		return 
	browser.find_element_by_id('j_username').send_keys(login)
	browser.find_element_by_id('j_password').send_keys(password)
	browser.find_element_by_id('submit').click()

	while True:
		browser.get(url)
		try:
			browser.find_element_by_css_selector('div[class*=\"merge-conflicted-message\"]')
			break
		except: pass
		merge_btn = browser.find_element_by_css_selector('button[class*=\"merge-button\"]')
		if merge_btn.get_attribute('aria-disabled') == 'false':
			merge_btn.click()
			browser.find_element_by_css_selector('button[class*=\"confirm-button\"]').click()
			break
		sleep(float(delay))


print 'Enter Bitbucket login: ',
login = raw_input()
print 'Enter Bitbucket password: ',
password = raw_input()
print 'Enter URL to pull request: ',
url = raw_input()
print 'Enter desired delay of merge attempts in seconds (optional, will be set to 10 by default):'
delay = raw_input()

print 'I am a Night Watcher! No pull requests will be left unmerged!'
if delay != '': start(login, password, url, delay)
else: start(login, password, url)
raw_input()
# id="commit-message" - input text
# class="aui-button aui-button-primary confirm-button" text (Megre) - click to merge.
# aui-button aui-button-primary confirm-button
# merge-conflicted-message