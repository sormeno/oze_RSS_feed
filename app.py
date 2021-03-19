from configs import RSS_config, SMTP_config,general_config, Selenium_config
import libs
import logging
import time
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO,
    handlers=[logging.FileHandler(general_config.LOG_FILENAME, 'a', 'utf-8')]
    )
logger = logging.getLogger('oze_RSS_feed')

start_time = time.time()
logger.info('\n\n--------------------------------------------Program execution started!')

msg_html = libs.rss.build_rss_message(RSS_config)
msg_html = msg_html + libs.selenium.build_selenium_message(Selenium_config)

smtp_client = libs.mail.SMTP(SMTP_config.HOST, SMTP_config.PORT, SMTP_config.MAIL_FROM, SMTP_config.PASSWORD)
smtp_client.send_email(SMTP_config.MAIL_TO, SMTP_config.MAIL_SUBJECT, msg_html_content=msg_html)
smtp_client.close()

logger.info(f'End of RSS program execution. Total time {time.time() - start_time}')





