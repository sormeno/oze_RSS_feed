import datetime
import libs
import requests
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger('RSS_feed.rss')

def build_rss_message(RSS_config):

    current_time = datetime.datetime.today() - datetime.timedelta(days=1)
    logger.info(f'Looking for news newer than {current_time}')

    msg_html = f"""
    <html>  
        <head></head>
        <body bgcolor="#FFFFFF">
            <p>Dzisiejszy OZE RSS news feed<br>"""


    for RSS in RSS_config.RSS_list:
        xml = libs.xml.XML(RSS.get('rss_url'))
        msg_html = f'{msg_html}<br>{RSS.get("title")}<br>\n'
        logger.info(f'Getting news from {RSS.get("rss_url")}')
        for elem in xml.parse_RSS_XML('channel/item','title','pubDate','link','description'):

            logger.info(f'Parsing article: {elem.get("title")}')
            if RSS.get('overwrite_pubdate'):
                logger.info(f'Cannot find pub_date. Extracting from article content.')
                pub_date = extract_pub_date(RSS.get('overwrite_pubdate'), elem.get('link'), RSS.get('date_fmt'))
            else:
                pub_date = elem.get('date')

            logger.info(f'Following pub_date found: {pub_date}. Converting to datetime type.')
            pub_date = datetime.datetime.strptime(pub_date, RSS.get('date_fmt')).replace(tzinfo=None)
            logger.info(f'Date converted to {pub_date}')

            if  pub_date > current_time:
                logger.info(f'{pub_date} is newer than {current_time}. Adding news \'{elem.get("title")}\' to message')
                msg_html = f'{msg_html} <a href=\"{elem.get("link")}\">{elem.get("title")}</a><br>\n--<br>'

    msg_html = f'{msg_html}</p></body</html>'
    logger.info(f'Building message completed. Message content:\n {msg_html}')
    return msg_html

def extract_pub_date(pub_date_markup, url, date_format):
    content = requests.get(url, allow_redirects=True).content
    parsed = BeautifulSoup(content,'html.parser')
    logger.info(f'Extracting pub_date from {url} with html markup: {pub_date_markup}')
    try:
        markup = parsed.find(*pub_date_markup).text
        markup = markup.replace('RI/PR24','n').replace('polskieradio24.pl','n').replace('RI/112','n').replace('fr/40','n') #todo remove this hard code
        logger.info(f'Following pub_date found: {markup}')
        pub_date = ''.join(list(filter(str.isdigit, markup.split('\n', 1)[0])))
        return pub_date
    except AttributeError:
        logger.warning(f'Cannot find pub_date on {url}')
        return datetime.datetime(2001, 1, 1).strftime(date_format)


