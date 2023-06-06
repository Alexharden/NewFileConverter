import os, time, psutil
import pyautogui, pyperclip
from EventLog.exception_handler import ExceptionHandler

"""harden
# 圖片下載路徑
m_login = r'./image/m_login.jpg' #判斷w是否開啟的圖
magic_box = r'./image/magicbox.jpg' #百寶箱的圖
m_C_Disk = r'./image/m_steelchannel.jpg' #c槽
m_fileconverter_folder = r'./image/m_fileconvented.jpg'  #轉檔資料夾
m_download_file_folder = r'./image/m_downloadfile.jpg' #下載資料夾
m_olf_image = r'./image/m_olfimage.jpg' #olf 檔案的圖
select_allpage = r'./image/selectallpage.jpg' #選取所有頁面
checkmark = r'./image/m_checkmark.jpg' #點所選取所有頁面 會打勾 來判斷是否點到了選取頁面    
import_landscape = r'./image/importlandscape.jpg' #水平匯入檔案
magic_tool = r'./image/m_magic_tool.jpg' #百寶箱的工具欄 來判斷是否匯入完成
page_menagement_menu = r'./image/pagemanagementmenu.jpg' #頁面管理
delete_page= r'./image/deletepage.jpg' #刪除頁面
confirm_delete = r'./image/confirmyes.jpg' #確認刪除 是
page1 = r'./image/page1.jpg' #判斷是否刪除掉空白第一頁

#存檔路徑
file_manager = r'./image/file_manager.jpg' #文件管理
save_as_image = r'./image/saveas.jpg' #另存新檔
C_Disk = r'./image/f_steelchannel.jpg' #c槽

f_fileconverter_folder = r'./image/f_fileconverter.jpg' 
f_converted_file_folder = r'./image/f_convertedfile.jpg' #轉檔資料夾
rename_olf_file = r'./image/rename_olffile.jpg' #重新命名
f_confirm_save = r'./image/f_confirm_save.jpg' #輸入檔案名稱後的 能不能點擊確認存檔的勾
save_success = r'./image/save_success.jpg' #判斷 檔案是否存檔完成
"""
m_login = r'./image/m_login.png' #判斷w是否開啟的圖
magic_box = r'./image/magicbox.png' #百寶箱的圖
m_C_Disk = r'./image/m_steelchannel.png' #c槽
m_fileconverter_folder = r'./image/m_fileconverted.png'  #轉檔資料夾
m_download_file_folder = r'./image/m_downloadfile.png' #下載資料夾
m_olf_image = r'./image/m_olfimage.png' #olf 檔案的圖
import_process = r"./image/importprocess.png" #loading圖
select_allpage = r'./image/selectallpage.png' #選取所有頁面
checkmark = r'./image/m_checkmark.png' #點所選取所有頁面 會打勾 來判斷是否點到了選取頁面    
import_landscape = r'./image/importlandscape.png' #水平匯入檔案
magic_tool = r'./image/m_magic_tool.png' #百寶箱的工具欄 來判斷是否匯入完成
page_menagement_menu = r'./image/pagemanagementmenu.png' #頁面管理
error_message = r"./image/importerror.png" #錯誤訊息
delete_page= r'./image/deletepage.png' #刪除頁面
confirm_delete = r'./image/confirmyes.png' #確認刪除 是
page1 = r'./image/page1.png' #判斷是否刪除掉空白第一頁

#存檔路徑
file_manager = r'./image/file_manager.png' #文件管理
save_as_image = r'./image/saveas.png' #另存新檔
C_Disk = r'./image/f_steelchannel.png' #c槽

f_fileconverter_folder = r'./image/f_fileconverter.png' 
f_converted_file_folder = r'./image/f_convertedfile.png' #轉檔資料夾
rename_olf_file = r'./image/rename_olffile.png' #重新命名
f_confirm_save = r'./image/f_confirm_save.png' #輸入檔案名稱後的 能不能點擊確認存檔的勾
save_success = r'./image/save_success.png' #判斷 檔案是否存檔完成

class AppControl: #白板上的操作
    def __init__(self):
        self.pgui = pyautogui
        self.ppc = pyperclip

    def launch_app(self, path):
        os.popen(path)
        try:
            self.icon_wait(m_login, True) #判斷w開啟了沒
            ExceptionHandler(msg= f"{path}已成功開啟.", exceptionLevel= "info")
        except:
            ExceptionHandler(msg= f"{path}開啟失敗", exceptionLevel= "critical")
       
    def close_app(self, appName):
        def get_processing():
            pids = psutil.pids()
            process = []
            for pid in pids:
                process.append(psutil.Process(pid).name())
            return process   
        try:
            while appName in get_processing(): #強制中指
                os.system(f"TASKKILL /F /IM {appName} /T")
                ExceptionHandler(msg = f"{appName}還未關閉", exceptionLevel= "info")
            else:
                ExceptionHandler(msg = f"找不到{appName}", exceptionLevel= "info")
        except:
            ExceptionHandler(msg = f"{appName}已關閉", exceptionLevel= "info")

    def type_write(self, content): #複製檔名貼上
        time.sleep(1)
        self.ppc.copy(content)
        time.sleep(1)
        self.pgui.hotkey("ctrl", "v")
    
    def is_icon_get(self, icon): #處理匯入出錯時用
        if self.pgui.locateCenterOnScreen(icon, confidence= 0.9) != None: #用圖片判斷
            return True
        else:
            return False

    def icon_click(self, icon): #點擊
        x, y = self.pgui.locateCenterOnScreen(icon, confidence= 0.9)
        self.pgui.moveTo(x, y)
        time.sleep(2)
        self.pgui.click()
        self.pgui.moveTo(50, 50)
    
    def icon_doubleClick(self, icon): #雙擊
        x, y = self.pgui.locateCenterOnScreen(icon, confidence= 0.9)
        self.pgui.moveTo(x, y)
        time.sleep(2)
        self.pgui.doubleClick()
        self.pgui.moveTo(50, 50)

    def icon_wait(self, waitObj, flag: bool, times = 120):
        "動態等待 True代表要等它出現 False反之"
        startTime = time.time()
        if flag == True:
            while self.pgui.locateCenterOnScreen(waitObj) == None:
                if time.time() - startTime > times:
                    ExceptionHandler(msg= "Timeout! Cannot see the element.", exceptionLevel= "critical")
                    raise
        else:
            while self.pgui.locateCenterOnScreen(waitObj) != None:
                if time.time() - startTime > times:
                    ExceptionHandler(msg= "Timeout! the element is still existing.", exceptionLevel= "critical")
                    raise