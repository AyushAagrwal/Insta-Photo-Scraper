from flask import Flask, render_template,request,redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import io
from PIL import Image
import imagehash
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

app = Flask(__name__)

options=webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("disable-blink-features=AutomationControlled")
# options.add_argument('--headless')
service=Service(executable_path='C:\Webdriver\chromedriver.exe')


driver = webdriver.Chrome(service=service, options=options) 

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']
    
    try:
        # Navigate to Instagram login page
        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        
        # Fill in the login form
        username_input = driver.find_element(By.XPATH,"//input[@name='username']")
        password_input = driver.find_element(By.XPATH,"//input[@name='password']")
        login_button = driver.find_element(By.XPATH,"//button[@type='submit']")

        username_input.send_keys(username)
        password_input.send_keys(password)
        
        # Submit the login form
        login_button.click()
        # time.sleep(5)
        driver.implicitly_wait(5)

        driver.find_element(By.XPATH,"//div[@class='_ac8f']//div").click()
        # Check if login was successful
        if driver.current_url == 'https://www.instagram.com/':
            # Perform your desired actions here after successful login
            return render_template('profile.html')
        else:
            # return render_template('fail.html')
            return 'Login Failed'

    except Exception as e:
        # Render an HTML page indicating login failure and display the error message
        return render_template('login_failed.html', error=str(e))

@app.route('/profile', methods=['GET'])
def profile():
    username = request.args.get('username')
    profile_url = f"https://www.instagram.com/{username}/"

    try:
        driver.get(profile_url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='xl565be x1m39q7l x1uw6ca5 x2pgyrj']//a"))
        )
        return render_template('scrap.html')
    except Exception as e:
    # Render an HTML page indicating an error occurred and display the error message
        return render_template('fail.html', error=str(e))
    
@app.route('/scrap_photos', methods=['POST'])
def scrap_photos_route():
    try:
        scrap_photos(driver)
        return 'Scraping photos successful', 200
    except Exception as e:
        message = "<h1>Scraping photos failed: Unable to find the specified element</h1>"
        return f'Scraping photos failed: {str(e)}', 500,message

def scrap_photos(driver):
    first_photo = driver.find_element(By.XPATH, "//div[@class='_aagw']")
    first_photo.click()
    photo_urls = set()
    unique_hashes = set()

    while True:
        try:
            bot_token = '5957670937:AAFmxIFd5vzdbSbrK3dpuhJtlvHjZ-9yeEk'
            chat_id = '592978820'
            next_arrow = driver.find_element(By.XPATH, "//div[@class=' _aaqg _aaqh']")
            next_arrow.click()
            time.sleep(0.5)
            driver.implicitly_wait(0.5)
            photos = driver.find_elements(By.XPATH, "//div[@class='_aagv']//img")

            for i in photos:
                lists = i.get_attribute('src')
                response = requests.get(lists)
                image_data = io.BytesIO(response.content)

                image = Image.open(image_data)
                image_hash = imagehash.average_hash(image)

                if image_hash not in unique_hashes:
                    photo_urls.add(lists)
                    unique_hashes.add(image_hash)

                    image_data.seek(0)
                    files = {'photo': ('image.jpg', image_data, 'image/jpeg')}
                    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
                    params = {'chat_id': chat_id}
                    response = requests.post(url, params=params, files=files)

                    if response.status_code == 200:
                        print("Sent to Telegram")
                    else:
                        print("Failed to send to Telegram")

                else:
                    print('Duplicate image:', lists)
        except NoSuchElementException:
            print("Error Occurred")
            break



if __name__ == '__main__':
    app.run(debug=True)