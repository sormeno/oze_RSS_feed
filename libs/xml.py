from urllib.request import urlopen
from urllib.request import Request
from xml.etree.ElementTree import parse
from configs.RSS_config import header
import logging
logger = logging.getLogger('RSS_feed.xml')

class XML:
    def __init__(self,url):
        self.url = url
        self.request = Request(url, headers = header)
        try:
            self.response = urlopen(self.request)
            logger.info(f'Connected with {self.url} with status {self.response.status}')
            self.parsed = parse(self.response)
            logger.info(f'XML parsed successfully')
            self.status = 'OK'
        except Exception as e:
            logger.warning(f'Cannot connect with {self.url} or cannot parse XML', exc_info=True)
            self.status = 'NOK'
            self.response = None
            self.parsed = None

    def parse_RSS_XML(self, items_list, title_label, date_label, link_label, description_label):
        news_list = []
        for item in self.parsed.iterfind(items_list):
            title = item.findtext(title_label)
            logger.info(f'Following title found: {title}')
            date = item.findtext(date_label)
            logger.info(f'Following date found: {date}')
            link = item.findtext(link_label)
            logger.info(f'Following link found: {link}')
            description = item.findtext(description_label)
            logger.info(f'Following description found: {description}')
            news_list.append({
                'title': title,
                'date': date,
                'link': link,
                'description': description
            })

        return news_list


