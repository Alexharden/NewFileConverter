from EventLog.exception_handler import ExceptionHandler
from Library.Website.web_control import WebControl
from Flow.create_driver import WebDriver
from Library.Function_Retry.Retry import RetryMechanism
from Element.Elements import Elements_FileConversion
from Library.System.File_Control import FileControl
from Library.Application.App_Control import *



def get_extension(fileName): #下載檔案的副檔名
    extension = "" #空字串儲存
    for i in range(len(fileName)-1, -1, -1): #下載下來的檔案名稱從最後一位數開始找
        extension += fileName[i] #每一次迴圈將最後一位字存入字串內
        if fileName[i] == ".": #如果找到. 則迴圈結束 表示找到了ˊ副檔名
            return "".join(reversed(extension)) #將字反轉 join將字合併 回傳副檔名

class GetFiles: #開啟.txt檔案
    def __init__(self, path): #開啟一個檔案(這邊是只存放失敗的txt檔案)
        self.Files = self.get_files(path)
    def get_files(self, path):
        with open (path, "r", encoding= "utf-8") as f: #開啟失敗的txt檔案
            files = f.readlines() #讀取失敗的檔案
            allfile = [] #存放讀取到的失敗的檔案名稱
            for i in range(len(files)): #迴圈 讀取完一行就換行
                files[i] = files[i].replace("\n", "") #
                allfile.append(files[i])
        print("開啟並讀取到失敗的檔案")
        return allfile

# class GetFiles: #開啟.txt檔案
#     def __init__(self, path): #開啟一個檔案(這邊是只存放失敗的txt檔案)
#         self.Files = self.get_files(path)
#     def get_files(self, path):
#         with open (path, "r", encoding= "utf-8") as f: #開啟失敗的txt檔案
#             allfile = [] #存放讀取到的失敗的檔案名稱
#             for i in f: #迴圈 讀取完一行就換行
#                 allfile.append(i.replace("\n", "")) #
#         print("成功讀取到失敗的檔案了")
#         return allfile

class Web_Flow: #整個網頁的流程
    def __init__(self):
        self.driver = WebDriver().Create_Driver() #呼叫創建一個webdriver
        self.wc = WebControl(self.driver) #用一個變數來存放 webdriver
        self.element = Elements_FileConversion(self.wc) #將網頁上所有需要用到的元素存入
        self.failFiles = GetFiles("./Failed_File/failed_files.txt").Files #開啟失敗的檔案的txt檔案 並讀取.Files
        self.fc = FileControl() #呼叫刪除檔案 創建資料夾 等待檔案下載
    def enter_webpage(self, url, acc, pwd): #網頁流程 輸入 網址 放大視窗 輸入帳號密碼 點擊登入
        self.wc.enter_target_page(url)
        self.wc.maximize_window()
        self.wc.element_send_keys(self.element.AccField, acc)
        self.wc.element_send_keys(self.element.PwdField, pwd)
        self.wc.element_click(self.element.LoginBtn)
        time.sleep(1)
    def newfilesname(self,taskIndex):
        time.sleep(2)
        self.createTime = self.element.CreateTime(taskIndex) #儲存要下載的檔案時間
        self.fileName = self.element.FileName(taskIndex) #儲存要下載的檔案名稱
    def download_file(self, taskIndex): #下載檔案
        self.wc.maximize_window() #放大視窗
        if self.createTime+self.fileName in self.failFiles:  #如果檔案時間+檔案名稱出現在失敗的txt中
            ExceptionHandler(msg= f"{self.createTime+self.fileName} is failed file.", exceptionLevel= "info")
            raise
        else:
            if self.element.States(taskIndex) == "Progress" or self.element.States(taskIndex) == "New": #狀態如果是這兩個 就會往下執行動作
                self.wc.element_click(self.element.downloadLink(taskIndex)) #點擊下載
                ExceptionHandler(msg= f"{self.createTime+self.fileName} 點擊檔案下載", exceptionLevel= "info")
                self.fc.file_wait("./Download_File/", get_extension(self.fileName)) #等待檔案下載完成
                ExceptionHandler(msg= f"{self.createTime+self.fileName} 檔案下載完成了", exceptionLevel= "info")
                self.wc.minimize_window() #縮小視窗
            else:
                ExceptionHandler(msg=f"{self.createTime+self.fileName} is 'Review' Task", exceptionLevel= "info")#這邊只是判斷如果檔案是Review 寫進去log較好判斷
                raise
    def upload_file(self, taskIndex): #上傳檔案
        self.wc.maximize_window() #放大視窗
        self.wc.element_send_keys(self.element.UploadBtn(taskIndex), os.path.join(os.path.abspath("./Convert_File/"), os.listdir("./Convert_File/")[0])) #從這個資料夾抓index[0]的檔案用send keys將檔案上傳
        while self.element.States(taskIndex) != "Review":#如果檔案=review 跳過這次
            pass 
    def turn_page(self): #點擊下一頁
        self.wc.element_click(self.element.nextPageBtn)
        time.sleep(3)
        ExceptionHandler(msg= "點擊下一頁", exceptionLevel= "info")
    def add_error_file(self): #錯誤檔案的建立時間+檔案名稱寫入失敗的txt
        self.fc.add_failed_file(self.createTime+self.fileName)
        ExceptionHandler(msg= f"{self.createTime+self.fileName} 此檔案有問題，寫入失敗的txt", exceptionLevel= "info")
    def finish_close_web(self):
        self.wc.close_webpage() #關閉網頁
        ExceptionHandler(msg= "關閉網頁", exceptionLevel= "info")
    def approve_icon(self,btn): #批准
        try:
            self.wc.element_click(self.element.SendBtn(btn))
            time.sleep(2)
            ExceptionHandler(msg= f"{self.createTime+self.fileName} 批准此檔案 ", exceptionLevel= "info")
        except:
            ExceptionHandler(msg= f"{self.createTime+self.fileName} 無法批准此檔案 ", exceptionLevel= "critical")
            raise

class Whiteboard_Flow: #白板的流程
    def __init__(self):
        self.ap = AppControl() #白板控制
        self.fc = FileControl() #呼叫刪除檔案 創建資料夾 等待檔案下載
    def launch_MVBW(self):
        self.ap.launch_app(r"C:\Program Files\ViewSonic\vBoard\vBoard.exe") #開啟白板
        ExceptionHandler(msg= "開啟白板", exceptionLevel= "info")
    def open_magicbox(self):
        try: #True 是東西出現 False 是東西消失
            self.ap.icon_wait(magic_box, True)
            self.ap.icon_click(magic_box)
            ExceptionHandler(msg= "有點到百寶箱", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到magicbox圖示，無法點擊", exceptionLevel= "critical")
            raise
    def magicbox_C_dick(self):
        try:
            self.ap.icon_wait(m_C_Disk, True)
            self.ap.icon_doubleClick(m_C_Disk)
            ExceptionHandler(msg= "有點到C槽", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到C槽圖示，無法點擊", exceptionLevel= "critical")
            raise
    def magicbox_fileConvert_folder(self):
        try:
            self.ap.icon_wait(m_fileconverter_folder, True)
            self.ap.icon_doubleClick(m_fileconverter_folder)
            ExceptionHandler(msg= "有點到FileConverter資料夾", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到FileConverter資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def magicbox_download_folder(self):
        try:
            self.ap.icon_wait(m_download_file_folder, True)
            self.ap.icon_doubleClick(m_download_file_folder)
            ExceptionHandler(msg= "有點到Download", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到Download資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def import_file(self):
        try:
            self.ap.icon_wait(m_olf_image, True)
            self.ap.icon_doubleClick(m_olf_image)
            ExceptionHandler(msg= "有點到下載檔案的圖示", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到欲下載檔案圖示，無法點擊", exceptionLevel= "critical")
            raise
    def import_error(self):
        try:
            self.ap.icon_wait(error_message, True, 5)
            ExceptionHandler(msg= "匯入失敗，無法匯入檔案", exceptionLevel="critical")
        except:
            ExceptionHandler(msg= "無錯誤", exceptionLevel="info")
        return self.ap.is_icon_get(error_message)
            
    def select_all_page(self):
        try:
            startTime = time.time()
            while time.time() - startTime < 120:
                if self.ap.is_icon_get(select_allpage): #120秒內抓到這張圖片出現 結束while 做點及
                    break
                elif self.ap.is_icon_get(error_message):  #如果遇到這張圖片去異常處理
                    raise
                elif time.time() - startTime >= 120: #超過120米都沒發現圖片 去異常處理
                    raise
            self.ap.icon_click(select_allpage)
            ExceptionHandler(msg= "有點到所有頁面按鍵", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到選取所有頁面按鍵，無法點擊", exceptionLevel= "critical")
            raise
    def landscape_image(self):
        try:
            self.ap.icon_wait(import_landscape, True)
            self.ap.icon_click(import_landscape)
            ExceptionHandler(msg= "有點到水平匯入按鍵", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到水平匯入按鍵，無法點擊", exceptionLevel= "critical")
            raise
    def wait_importing(self):
        try:
            time.sleep(3)
            self.ap.icon_wait(import_landscape, False)
            self.ap.icon_wait(magic_tool, False)
            ExceptionHandler(msg= "匯入成功", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "超時，匯入失敗.", exceptionLevel= "critical")
            raise
    def open_page_management(self):
        try:
            self.ap.icon_wait(page_menagement_menu, True)
            self.ap.icon_click(page_menagement_menu)
            ExceptionHandler(msg= "有點到頁面管理圖示", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到頁面管理圖示，無法點擊", exceptionLevel= "critical")
            raise
    def delete_first_page(self):
        try:
            self.ap.icon_wait(delete_page, True)
            self.ap.icon_click(delete_page)
            ExceptionHandler(msg= "有點到刪除頁面圖示", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到刪除頁面圖示，無法點擊", exceptionLevel= "critical")
            raise
    def confirm_delete(self):
        try:
            self.ap.icon_wait(confirm_delete, True)
            self.ap.icon_click(confirm_delete)
            ExceptionHandler(msg= "有點到確認按鍵", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到確認按鍵，無法點擊", exceptionLevel= "critical")
            raise
    def wait_deleting(self):
        try:
            self.ap.icon_wait(page1, True)
            self.ap.icon_click(page1)
            ExceptionHandler(msg= "有點到第一頁頁面管理圖是", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到第一頁頁面管理圖示，無法點擊", exceptionLevel= "critical")
            raise
    def open_file_management(self):
        try:
            self.ap.icon_wait(file_manager, True)
            self.ap.icon_click(file_manager)
            ExceptionHandler(msg= "有點到檔案管理", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到檔案管理圖示，無法點擊", exceptionLevel= "critical")
            raise
    def save_as_file(self):
        try:
            self.ap.icon_wait(save_as_image, True)
            self.ap.icon_click(save_as_image)
            ExceptionHandler(msg= "儲存流程 有點到存檔圖示", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到存檔圖示，無法點擊", exceptionLevel= "critical")
            raise
    def filemanager_C_disk(self):
        try:
            self.ap.icon_wait(C_Disk, True)
            self.ap.icon_doubleClick(C_Disk)
            ExceptionHandler(msg= "儲存流程 有點到C槽圖示", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到C槽圖示，無法點擊", exceptionLevel= "critical")
            raise
    def filemanager_fileConvert_folder(self):
        try:
            self.ap.icon_wait(f_fileconverter_folder, True)
            self.ap.icon_doubleClick(f_fileconverter_folder)
            ExceptionHandler(msg= "儲存流程 有點到FileConverter", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到FileConverter資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def filemanager_convert_folder(self):
        try:
            self.ap.icon_wait(f_converted_file_folder, True)
            self.ap.icon_doubleClick(f_converted_file_folder)
            ExceptionHandler(msg= "儲存流程 有點到Converted", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到Converted資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def save_olf_file(self):
        try:
            self.ap.icon_wait(rename_olf_file, True)
            self.ap.icon_click(rename_olf_file)
            self.ap.type_write("converted") #預設儲存轉檔完的名稱
            ExceptionHandler(msg= "儲存流程 有點到輸入檔名欄位", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到輸入檔名欄位，無法點擊", exceptionLevel= "critical")
            raise
            
        try:
            self.ap.icon_wait(f_confirm_save, True)
            self.ap.icon_click(f_confirm_save)
            ExceptionHandler(msg= "儲存流程 有點到存檔打勾圖示", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "找不到確認存檔打勾圖示，無法點擊", exceptionLevel= "critical")
            raise
        
        try:
            self.fc.file_wait("./Convert_File/", ".olf")
            ExceptionHandler(msg= "檔案儲存成功", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "超時！存檔時間太長", exceptionLevel= "critical")
            raise
    def finish_close_app(self): #關閉白板
        self.ap.close_app("vBoard.exe")
            
# class ConversionFlow:
#     def __init__(self):
        
