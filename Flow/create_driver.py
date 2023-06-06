from Library.Website.Chromedriver_version import DownloadFitChromeDrive
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from EventLog.exception_handler import ExceptionHandler
import os

class WebDriver: #開啟web driver
    def Create_Driver(self):
        try:
            options = webdriver.ChromeOptions()
            prefs = {
            'profile.default_content_setting_values':
            {
                'notifications': 2,
            },
            'profile.default_content_settings.popups': 0, 
            'download.default_directory': os.path.abspath('Download_File'),
            "download.prompt_for_download": False,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False}
            options.add_experimental_option('prefs', prefs)
            options.add_argument('--disable-gpu')
            options.add_argument('--lang=zh-TW')
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--windows-size=800x600')
            # options.add_argument('--start-minimized')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-features=InterestCohort')
            # options.add_argument('--log-level=1')
            #抓出與本機端chrome相同版本的版號
            driver  = webdriver.Chrome(ChromeDriverManager(version= DownloadFitChromeDrive().downloadVersion).install(), options= options)
            # driver = webdriver.Chrome(options= options)
            # ExceptionHandler(msg= "Successfully open browser driver. 成功開啟瀏覽器驅動器", exceptionLevel= "info")
            return driver
        except:
            ExceptionHandler(msg= "Cannot open browser driver. 無法開啟瀏覽器驅動器", exceptionLevel= "critical")