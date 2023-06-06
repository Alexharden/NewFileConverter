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
        return allfile

class Web_Flow: #整個網頁的流程
    def __init__(self):
        self.driver = WebDriver().Create_Driver()
        self.wc = WebControl(self.driver)
        self.element = Elements_FileConversion(self.wc)
        self.failFiles = GetFiles("./Failed_File/failed_files.txt").Files
        self.fc = FileControl()
    def enter_webpage(self, url, acc, pwd):
        self.wc.enter_target_page(url)
        self.wc.maximize_window()
        self.wc.element_send_keys(self.element.AccField, acc)
        self.wc.element_send_keys(self.element.PwdField, pwd)
        self.wc.element_click(self.element.LoginBtn)
    def download_file(self, taskIndex):
        self.wc.maximize_window()
        self.createTime = self.element.CreateTime(taskIndex)
        self.fileName = self.element.FileName(taskIndex)
        if self.createTime+self.fileName in self.failFiles:
            ExceptionHandler(msg= f"{self.createTime+self.fileName} is failed file.", exceptionLevel= "info")
            raise
        else:
            if self.element.States(taskIndex) == "Progress" or self.element.States(taskIndex) == "New":
                self.wc.element_click(self.element.downloadLink(taskIndex))
                self.fc.file_wait("./Download_File/", get_extension(self.fileName))
                self.wc.minimize_window()
            else:
                ExceptionHandler(msg=f"{self.createTime+self.fileName} is 'Review' Task", exceptionLevel= "info")
                raise
    def upload_file(self, taskIndex):
        self.wc.maximize_window()
        self.wc.element_send_keys(self.element.UploadBtn(taskIndex), os.path.join(os.path.abspath("./Convert_File/"), os.listdir("./Convert_File/")[0]))
        while self.element.States(taskIndex) != "Review":
            pass
    def turn_page(self):
        self.wc.element_click(self.element.nextPageBtn)
        time.sleep(3)
    def add_error_file(self):
        self.fc.add_failed_file(self.createTime+self.fileName)
    def finish_close_web(self):
        self.wc.close_webpage()
        ExceptionHandler(msg= "轉檔上傳流程結束", exceptionLevel= "info")

class Whiteboard_Flow: #白板的流程
    def __init__(self):
        self.ap = AppControl()
        self.fc = FileControl()
    def launch_MVBW(self):
        self.ap.launch_app(r"C:\Program Files\ViewSonic\vBoard\vBoard.exe")
    def open_magicbox(self):
        try:
            self.ap.icon_wait(magic_box, True)
            self.ap.icon_click(magic_box)
        except:
            ExceptionHandler(msg= "找不到magicbox圖示，無法點擊", exceptionLevel= "critical")
            raise
    def magicbox_C_dick(self):
        try:
            self.ap.icon_wait(m_C_Disk, True)
            self.ap.icon_doubleClick(m_C_Disk)
        except:
            ExceptionHandler(msg= "找不到C槽圖示，無法點擊", exceptionLevel= "critical")
            raise
    def magicbox_fileConvert_folder(self):
        try:
            self.ap.icon_wait(m_fileconverter_folder, True)
            self.ap.icon_doubleClick(m_fileconverter_folder)
        except:
            ExceptionHandler(msg= "找不到FileConverter資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def magicbox_download_folder(self):
        try:
            self.ap.icon_wait(m_download_file_folder, True)
            self.ap.icon_doubleClick(m_download_file_folder)
        except:
            ExceptionHandler(msg= "找不到Download資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def import_file(self):
        try:
            self.ap.icon_wait(m_olf_image, True)
            self.ap.icon_doubleClick(m_olf_image)
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
            self.ap.icon_wait(magic_tool, False)
            self.ap.icon_wait(select_allpage, True)
            self.ap.icon_click(select_allpage)
        except:
            ExceptionHandler(msg= "找不到選取所有頁面按鍵，無法點擊", exceptionLevel= "critical")
            raise
    def landscape_image(self):
        try:
            self.ap.icon_wait(import_landscape, True)
            self.ap.icon_click(import_landscape)
        except:
            ExceptionHandler(msg= "找不到水平匯入按鍵，無法點擊", exceptionLevel= "critical")
            raise
    def wait_importing(self):
        try:
            self.ap.icon_wait(import_landscape, False)
            self.ap.icon_wait(magic_tool, False)
            ExceptionHandler(msg= "匯入成功", exceptionLevel="info")
        except:
            ExceptionHandler(msg= "超時，匯入失敗.", exceptionLevel= "critical")
            raise
    def open_page_management(self):
        try:
            time.sleep(5)
            self.ap.icon_wait(page_menagement_menu, True)
            self.ap.icon_click(page_menagement_menu)
        except:
            ExceptionHandler(msg= "找不到頁面管理圖示，無法點擊", exceptionLevel= "critical")
            raise
    def delete_first_page(self):
        try:
            self.ap.icon_wait(delete_page, True)
            self.ap.icon_click(delete_page)
        except:
            ExceptionHandler(msg= "找不到刪除頁面圖示，無法點擊", exceptionLevel= "critical")
            raise
    def confirm_delete(self):
        try:
            self.ap.icon_wait(confirm_delete, True)
            self.ap.icon_click(confirm_delete)
        except:
            ExceptionHandler(msg= "找不到確認按鍵，無法點擊", exceptionLevel= "critical")
            raise
    def wait_deleting(self):
        try:
            self.ap.icon_wait(page1, True)
            self.ap.icon_click(page1)
        except:
            ExceptionHandler(msg= "找不到第一頁頁面管理圖示，無法點擊", exceptionLevel= "critical")
            raise
    def open_file_management(self):
        try:
            self.ap.icon_wait(file_manager, True)
            self.ap.icon_click(file_manager)
        except:
            ExceptionHandler(msg= "找不到檔案管理圖示，無法點擊", exceptionLevel= "critical")
            raise
    def save_as_file(self):
        try:
            self.ap.icon_wait(save_as_image, True)
            self.ap.icon_click(save_as_image)
        except:
            ExceptionHandler(msg= "找不到存檔圖示，無法點擊", exceptionLevel= "critical")
            raise
    def filemanager_C_disk(self):
        try:
            self.ap.icon_wait(C_Disk, True)
            self.ap.icon_doubleClick(C_Disk)
        except:
            ExceptionHandler(msg= "找不到C槽圖示，無法點擊", exceptionLevel= "critical")
            raise
    def filemanager_fileConvert_folder(self):
        try:
            self.ap.icon_wait(f_fileconverter_folder, True)
            self.ap.icon_doubleClick(f_fileconverter_folder)
        except:
            ExceptionHandler(msg= "找不到FileConverter資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def filemanager_convert_folder(self):
        try:
            self.ap.icon_wait(f_converted_file_folder, True)
            self.ap.icon_doubleClick(f_converted_file_folder)
        except:
            ExceptionHandler(msg= "找不到Converted資料夾圖示，無法點擊", exceptionLevel= "critical")
            raise
    def save_olf_file(self):
        try:
            self.ap.icon_wait(rename_olf_file, True)
            self.ap.icon_click(rename_olf_file)
            self.ap.type_write("converted")
        except:
            ExceptionHandler(msg= "找不到輸入檔名欄位，無法點擊", exceptionLevel= "critical")
            raise
            
        try:
            self.ap.icon_wait(f_confirm_save, True)
            self.ap.icon_click(f_confirm_save)
        except:
            ExceptionHandler(msg= "找不到確認存檔圖示，無法點擊", exceptionLevel= "critical")
            raise
        
        try:
            self.fc.file_wait("./Convert_File/", ".olf")
        except:
            ExceptionHandler(msg= "超時！存檔時間太長", exceptionLevel= "critical")
            raise
    def finish_close_app(self):
        self.ap.close_app("vBoard.exe")
            
# class ConversionFlow:
#     def __init__(self):
        
