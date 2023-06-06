import logging
import traceback
import os

class ExceptionHandler: #異常處理
    def __init__(self, msg: str, exceptionLevel: str):
        self.msg = msg
        self.exceptionLevel = exceptionLevel
        self.FORMAT = '\n%(asctime)s %(levelname)s: %(message)s' #格式化字串
        self.DATE_FORMAT = '%Y%m%d %H:%M:%S' #格式化日期
        self.level_recognizer()
        logging.basicConfig(level=self.level, format=self.FORMAT, datefmt= self.DATE_FORMAT, filemode="a+", encoding= "utf-8", filename= os.path.abspath("EventLog/Exception.log")) #將錯誤寫進
        self.record_logs()
        print(msg)
        
    def level_recognizer(self):  #設定問題等級
        if self.exceptionLevel.lower() == "debug": #診斷問題
            self.level = logging.DEBUG
        elif self.exceptionLevel.lower() == "info": #程式正常進行
            self.level = logging.INFO 
        elif self.exceptionLevel.lower() == "warning": #有些問題 但程式仍可正常執行
            self.level = logging.WARNING
        elif self.exceptionLevel.lower() == "error": #某些功能無法正常執行
            self.level = logging.ERROR 
        elif self.exceptionLevel.lower() == "critical": #嚴重錯誤 程式無法執行
            self.level = logging.CRITICAL
            
    def record_logs(self): #記錄問題
        if self.exceptionLevel.lower() == "debug":
            logging.debug(self.msg, exc_info= True)
        elif self.exceptionLevel.lower() == "info":
            logging.info(self.msg, exc_info= True)
        elif self.exceptionLevel.lower() == "warning":
            logging.warning(self.msg, exc_info= True)
        elif self.exceptionLevel.lower() == "error":
            logging.error(self.msg, exc_info= True)
        elif self.exceptionLevel.lower() == "critical":
            logging.critical(self.msg, exc_info= True)