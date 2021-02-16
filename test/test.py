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

		###########################################
		## Test with correct mail and password
		self.netflix_login_test("kose.dogukan@hotmail.com", "dogukan")
		time.sleep(0.2)
		
		main_text = self.driver.find_element_by_id("main_menu_text")
		assert main_text.text == "Signed In", "Login with correct mail and password failed."

		log_out_button = self.driver.find_element_by_id("logout")
		log_out_button.click();
		time.sleep(0.2)
		##
		###########################################

		###########################################
		## Test with wrong mail and wrong password
		self.netflix_login_test("wrong_email@hotmail.com", "wrongPassword")
		time.sleep(0.2)

		assert self.driver.switch_to.alert.text == "Invalid Credentials", "Login with wrong mail and password failed."
		self.driver.switch_to.alert.accept();
		##
		###########################################

		##########################################
		## Test with empty mail and password
		self.netflix_login_test("", "")
		time.sleep(0.2)

		assert self.driver.switch_to.alert.text == "Empty Credentials", "Login with empty mail and password failed."
		self.driver.switch_to.alert.accept();
		##
		###########################################

		###########################################				
		## Test with remember me check button when it is true
		self.netflix_remember_me_test("kose.dogukan@hotmail.com", "dogukan", True)
		##
		###########################################

		###########################################				
		## Test with remember me check button when it is false
		self.netflix_remember_me_test("kose.dogukan@hotmail.com", "dogukan", False)
		##
		##########################################
		time.sleep(0.2)
		self.change_password_test("kose.dogukan@hotmail.com", "d")

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

	def netflix_remember_me_test(self, email, password, remember_me):

		try:
			email_input = self.driver.find_element_by_id("email")
			password_input = self.driver.find_element_by_id("password")
			remember_me_check_box = self.driver.find_element_by_id("checkbox_remember_me")
			submit_button = self.driver.find_element_by_id("submit")

			if (remember_me_check_box.is_selected() and remember_me == False):
				remember_me_check_box.click()
			if (not remember_me_check_box.is_selected() and remember_me == True):
				remember_me_check_box.click()

			email_input.clear()
			email_input.send_keys(email)
			password_input.clear()
			password_input.send_keys(password)

			time.sleep(0.5)
		
			submit_button.click()
			time.sleep(0.5)

			log_out_button = self.driver.find_element_by_id("logout")
			log_out_button.click();
			time.sleep(0.5)	

			last_email_input = self.driver.find_element_by_id("email").get_attribute('value')
			last_password_input = self.driver.find_element_by_id("password").get_attribute('value')

			if (remember_me):
				assert (last_email_input == email), "Remember me check box test failed, cannot remember mail"
				assert (last_password_input == password), "Remember me check box test failed, cannot remember password"
			else:
				assert (last_email_input == ""), "Remember me check box test failed. Remember_me is not checked but it remembered email"
				assert (last_password_input == ""), "Remember me check box test failed. Remember_me is not checked but it remembered password"

		except Exception as e:
			print(str(e))

	def change_password_test(self, email, newpassword):
		try:
			need_help_link = self.driver.find_element_by_link_text('Need help?')
			time.sleep(0.5)
			need_help_link.click()
			email_input = self.driver.find_element_by_id("email")
			newpassword_input = self.driver.find_element_by_id("password")
			button_element = self.driver.find_element_by_id("submitEmail")
    
			email_input.clear()
			email_input.send_keys(email)
			newpassword_input.clear()
			newpassword_input.send_keys(newpassword)
			button_element.click()
			time.sleep(0.5)

			assert self.driver.switch_to.alert.text == "Your password is successfully changed!"
			self.driver.switch_to.alert.accept()
			time.sleep(0.5)

			email_input = self.driver.find_element_by_id("email")
			password_input = self.driver.find_element_by_id("password")
			button_element = self.driver.find_element_by_id("submit")

			email_input.clear()
			email_input.send_keys(email)
			password_input.clear()
			password_input.send_keys(newpassword)
			button_element.click()
			time.sleep(0.5)

			assert self.driver.find_element_by_id("main_menu_text").text == "Signed In"

			time.sleep(0.5)

			log_out_button = self.driver.find_element_by_id("logout")
			log_out_button.click()

		except Exception as e:
			print(str(e))

netflixWebPageTester = NetflixWebPageTester();
netflixWebPageTester.run_tests();
