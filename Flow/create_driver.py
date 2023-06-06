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
                'notifications': 2, #封鎖網站通知設定
            },
            'profile.default_content_settings.popups': 0,  #封鎖彈跳視窗 
            'download.default_directory': os.path.abspath('Download_File'), #下載檔案的路徑
            "download.prompt_for_download": False,  #封鎖下載的彈跳視窗
            "safebrowsing_for_trusted_sources_enabled": False, #禁用受信任來源安全瀏覽
            "safebrowsing.enabled": False} #禁用安全瀏覽功能
            options.add_experimental_option('prefs', prefs)
            options.add_argument('--disable-gpu') #禁止使用gpu
            options.add_argument('--lang=zh-TW') #設定成繁體中文
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox') #禁止用沙盒
            options.add_argument('--windows-size=800x600') #瀏覽器大小
            # options.add_argument('--start-minimized')
            options.add_argument('--disable-dev-shm-usage') #禁用共享記憶體
            options.add_argument('--remote-debugging-port=9222') #遠端窗口設定9222
            options.add_argument('--disable-blink-features=AutomationControlled') #用自動化控制的 Blink 功
            options.add_argument('--disable-features=InterestCohort')# 禁用興趣群體功能 google的廣告
            # options.add_argument('--log-level=1')
            #抓出與本機端chrome相同版本的版號
            driver  = webdriver.Chrome(ChromeDriverManager(version= DownloadFitChromeDrive().downloadVersion).install(), options= options) #啟動
            # driver = webdriver.Chrome(options= options)
            # ExceptionHandler(msg= "Successfully open browser driver. 成功開啟瀏覽器驅動器", exceptionLevel= "info")
            return driver
        except:
            ExceptionHandler(msg= "Cannot open browser driver. 無法開啟瀏覽器驅動器", exceptionLevel= "critical")