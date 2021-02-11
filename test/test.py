import time
import datetime
from selenium import webdriver
import os
import platform

class NetflixWebPageTester: 
	def __init__(self):

		super().__init__()
		self.URL = "file://" + os.getcwd()
		self.URL = self.URL[:-5] + "/src"
		self.pageURL = self.URL + "/index.html"
		self.class_name = 'LoginPageTest'
		self.setup()

	def setup(self):
		try:
			if (platform.system() == "Windows"):
				self.driver = webdriver.Chrome('chromedriver.exe')
			else:
				self.driver = webdriver.Chrome('chromedriver')
		except:
			raise Exception("Error occured about chromedriver. " + 
				"You might need to install another chromedriver that supported by your system.")

	def run_tests(self):

		## Run chrome
		self.driver.get(self.pageURL)
		time.sleep(2)

		## Click sign in button
		sign_in_button = self.driver.find_element_by_id("sign_in_button")
		sign_in_button.click();
		time.sleep(0.2)

		## Test with correct mail and password
		self.netflix_login_test("kose.dogukan@hotmail.com", "dogukan")
		time.sleep(0.2)
		
		main_text = self.driver.find_element_by_id("main_menu_text")
		assert main_text.text == "Signed In", "Login with correct mail and password failed."

		log_out_button = self.driver.find_element_by_id("logout")
		log_out_button.click();
		time.sleep(0.2)

		## Test with wrong mail and wrong password
		self.netflix_login_test("wrong_email@hotmail.com", "wrongPassword")
		time.sleep(0.2)

		assert self.driver.switch_to.alert.text == "Invalid Credentials", "Login with wrong mail and password failed."
		self.driver.switch_to.alert.accept();

		## Test with empty mail and password
		self.netflix_login_test("", "")
		time.sleep(0.2)

		assert self.driver.switch_to.alert.text == "Empty Credentials", "Login with empty mail and password failed."
		self.driver.switch_to.alert.accept();

	def netflix_login_test(self, email, password):

		try:
			email_input = self.driver.find_element_by_id("email")
			password_input = self.driver.find_element_by_id("password")
			submit_button = self.driver.find_element_by_id("submit")

			email_input.clear()
			email_input.send_keys(email)
			password_input.clear()
			password_input.send_keys(password)

			time.sleep(0.2)
			submit_button.click()
			time.sleep(3)

		except Exception as e:
			print(str(e))

         

netflixWebPageTester = NetflixWebPageTester();
netflixWebPageTester.run_tests();