from Library.Website.web_control import WebControl
from Library.Function_Retry.Retry import RetryMechanism

class Elements_FileConversion: #取得元素
    def __init__(self, webControl: WebControl):
        self.wc = webControl
    @property #將方法轉換成屬性 再呼叫的時候就不用加上 ()
    def AccField(self): return self.wc.get_element("//input[@placeholder='帳號']") #獲取帳號輸入框的元素
    @property
    def PwdField(self): return self.wc.get_element( "//input[@placeholder='密碼']") #獲取密碼輸入框的元素
    @property
    def LoginBtn(self): return self.wc.get_element("//button[text()='登入']") #獲取登入按鈕的元素
    @property
    def GetAllTasks(self): return self.wc.get_elements("//tbody/tr") #獲取所有任務的元素列表

    def CreateTime(self, index): return self.wc.subElement_get(self.GetAllTasks[index], "./td")[1].text #根據索引獲取指定任務的創建時間

    def FileName(self, index): return self.wc.subElement_get(self.GetAllTasks[index], "./td")[3].text #據索引獲取指定任務的檔案名稱

    def States(self, index): return self.wc.subElement_get(self.GetAllTasks[index], ".//button/span")[0].text #根據索引獲取指定任務的狀態

    def downloadLink(self, index): return self.wc.subElement_get(self.GetAllTasks[index], ".//td/a[text()='原檔']")[0] #根據索引獲取指定任務的下載連結。
    
    def UploadBtn(self, index): return self.wc.subElement_get(self.GetAllTasks[index], ".//p-fileupload//input")[0] #根據索引獲取指定任務的上傳按鈕

    def SendBtn(self, index): return self.wc.subElement_get(self.GetAllTasks[index], ".//p-radiobutton//span")[0] #根據索引獲取指定任務的批准
    
    @property
    def pages(self): return self.wc.get_elements(f"//span/a[text()]") #獲取所有頁面的元素列表
    @property
    def nextPageBtn(self): return self.wc.get_elements("//a/span")[2] #獲取下一頁按鈕的元素

