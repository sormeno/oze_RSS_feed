import datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import logging
logger = logging.getLogger('RSS_feed.selenium')

def build_selenium_message(Selenium_config):

    current_time = datetime.datetime.today() - datetime.timedelta(days=1)
    logger.info(f'Starting Selenium news feed.')
    logger.info(f'Looking for news newer than {current_time}')

    msg_html = f"""
    <html>  
        <head></head>
        <body bgcolor="#FFFFFF">"""

    logger.info(f'Initializing webdriver')
    chrome = webdriver.Chrome(options=options(Selenium_config) , executable_path=Selenium_config.webdriver_path)

    for site in Selenium_config.Selenium_RSS_list:
        chrome.get(site.get('url'))
        msg_html = f'{msg_html}<br>{site.get("title")}<br>\n'
        logger.info(f'Getting news from {site.get("url")}')

        index = chrome.find_element_by_xpath(site.get('index_selector'))
        newses = index.find_elements_by_xpath(site.get('news_selector'))

        for news in newses:
            title = news.find_element_by_tag_name(site.get('news_title_selector')).get_attribute('innerHTML')
            pub_date = datetime.datetime.strptime(news.find_element_by_tag_name(site.get('news_date_selector')).get_attribute('innerHTML'),site.get('date_fmt'))
            url = news.find_element_by_tag_name(site.get('news_url_selector')).get_attribute('href')
            if  pub_date > current_time:
                logger.info(f'{pub_date} is newer than {current_time}. Adding news \'{title}\' to message')
                msg_html = f'{msg_html} <a href=\"{url}\">{title}</a><br>\n--<br>'

        chrome.close()

    msg_html = f'{msg_html}</p></body</html>'
    logger.info(f'Building Selenium message completed. Message content:\n {msg_html}')
    return msg_html


def options(Selenium_config):
    options = Options()
    #options.binary_location = Selenium_config.chrome_location
    logger.info(f'Setting selenium options.')
    for elem in Selenium_config.selenium_config:
        options.add_argument(elem)
        logger.info(f'Options {elem} added')
    return options