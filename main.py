import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import random

# Setup log file
logging.basicConfig(filename='/home/william/PycharmProjects/ApartmentWebCrawler/main.log',
                    filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Script started...')


# Accept consent cookies
def accept_cookies(driver):
    try:
        driver.find_element_by_xpath('//*[@id="cmpbntyestxt"]').click()
    except NoSuchElementException:
        pass
        #print('Cookies already accepted')


def accept_safety_agreement(driver):
    try:
        driver.find_element_by_xpath("//*[@id='sicherheit_bestaetigung']").click()
    except (ElementNotInteractableException, NoSuchElementException):
        pass
        #print('Already read safety agreement')


# Webpage parameters
base_site = "https://www.wg-gesucht.de"
ext_site = "/wohnungen-in-Berlin.8.2.1.0.html?offer_filter=1&city_id=8&noDeact=1&categories[]=2&rent_types[]"\
           "=2&sMin=50&rMax=1100&ot[]=85079&ot[]=151&ot[]=165&ot[]=185&rmMin=2&rmMax=4&exc=2"

# Setup remote control browser
crawler_loc = '/home/william/PycharmProjects/ApartmentWebCrawler'
fireFoxOptions = webdriver.FirefoxOptions()
#fireFoxOptions.add_argument("--headless")  # Runs without browser pop-up
browser = webdriver.Firefox(executable_path='/home/william/Webdriver/bin/geckodriver',
                            log_path=crawler_loc + '/geckodriver.log',
                            firefox_options=fireFoxOptions)
browser.get(base_site)

try:
    accept_cookies(browser)
    browser.get(base_site + ext_site)
    browser.implicitly_wait(random.randint(15, 30))

    # Go to login pop-up
    browser.find_element_by_xpath("//*[contains(text(), 'Login')]").click()

    # Accept cookies again (Not always necessary?)
    accept_cookies(browser)

    # Login to website
    browser.implicitly_wait(random.randint(20, 30)) # Need to wait for elements to be loaded
    username = browser.find_element_by_id("login_email_username")
    password = browser.find_element_by_id("login_password")

    browser.implicitly_wait(random.randint(20, 30))
    username.send_keys("willbakermorrison@gmail.com")
    password.send_keys("vines9")
    browser.find_element_by_id("login_submit").click()

    # Accept cookies again (Not always necessary?)
    accept_cookies(browser)

    # Find parent elements to ad cards
    parent_elements = browser.find_elements_by_xpath("//*[@class='wgg_card offer_list_item  ']")

    # Find uncontacted links
    uncontacted_links = []
    for current_element in parent_elements:

        # Find if they have been contacted (using contacted image ribbon)
        localElement = current_element.find_element_by_css_selector("div>span")
        if localElement.get_attribute("class") != 'ribbon-contacted':  # If not contact

            # Find link to page
            element2 = current_element.find_element_by_css_selector('div>a')
            uncontacted_links.append(element2.get_attribute("href"))

    # Are these filtered by district?

    # If new ads, send messages to them
    if len(uncontacted_links) > 0:
        logging.info(str(len(uncontacted_links)) + ' new ad(s) online')

        # Loop through uncontacted links
        for current_link in uncontacted_links:
            logging.info('Looking at ad: ' + current_link)
            print('Looking at ad: ' + current_link)

            # Open link
            browser.get(current_link)

            # Get ad titlẹ and check for WBS
            ad_title = browser.find_element_by_id("sliderTopTitle").text
            if "wbs" in ad_title or "WBS" in ad_title:
                logging.info('WBS ad - cancelled')
                print('WBS ad - cancelled')

            else:
                # Get ad owner name
                rhs_element = browser.find_element_by_id("rhs_column")
                ad_owner_name = rhs_element.find_element_by_class_name('mb10').text
                ad_owner_name = ad_owner_name.replace('ist gerade online', '').replace("\n", "")  # Remove additional text
                logging.info('Ad owner:' + ad_owner_name)
                print('Ad owner:' + ad_owner_name)

                # Get ad street name
                main_column_element = browser.find_element_by_id("main_column")
                street_name = main_column_element.find_element_by_xpath("//a[@href='#mapContainer']").text.split('\n')[0]
                logging.info('Street name:' + street_name)
                print('Street name:' + street_name)

                try:
                    # Move to message page
                    browser.find_element_by_xpath('//a[contains(@href,"nachricht-senden")]').click()

                    # Click read safety agreement
                    accept_safety_agreement(browser)

                    # Write message
                    message = """Sehr geehrte/r """ + ad_owner_name + """,\n\nMeine Freundin Nora und ich sind sehr""" \
                              """ an Ihrer Wohnung in der """ + street_name + """ interessiert und würden gerne einen""" \
                              """ Besichtigungstermin mit Ihnen vereinbaren. Zunächst ein bisschen über uns:\n\nIch bin""" \
                              """ Engländer, lebe seit 5 Jahren in Berlin und arbeite als Dozent an einer Berliner""" \
                              """ Universität. Meine Partnerin hat eine Festanstellung als wissenschaftliche Mitarbeiterin""" \
                              """ und Doktorandin. Wir leben seit zwei Jahren in Kreuzberg und suchen für die nächsten""" \
                              """ Jahre eine größere Wohnung.\n\nWir haben alle Bewerbungsunterlagen sowohl digital als""" \
                              """ auch ausgedruckt jederzeit bereit.\n\nSie können mich entweder hier, via Email""" \
                              """ (williambakermorrison@posteo.de) oder telefonisch unter der Nummer 017658903116""" \
                              """ erreichen.\n\nMit freundlichen Grüßen,\nWill Baker Morrison und Nora Delvendahl"""

                    # Setup message
                    logging.info('Sending message')
                    print('Sending message')
                    browser.implicitly_wait(random.randint(20, 30))  # Need to wait for elements to be loaded
                    submit_message = browser.find_element_by_id("message_input")
                    submit_message.send_keys(message)

                    # Send message
                    browser.find_element_by_css_selector('button.create_new_conversation:nth-child(1)').click()

                except NoSuchElementException:
                    logging.info('No message button - Ad probably disabled')

    else:
        logging.info('No new apartment ads')
        # print('No new apartment ads')

finally:
    # logging.info('Some error occurred - closed browser')
    browser.quit()
