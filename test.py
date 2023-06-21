from Flow.Conversion_Flow import Web_Flow
from Flow.Conversion_Flow import Whiteboard_Flow
from Flow.Conversion_Flow import GetFiles
import time, threading



class TestFileConversion:
    def __init__(self):
        self.wf = Web_Flow()
        self.wbf = Whiteboard_Flow()   
    def start_web_download_flow(self, taskIndex):
        try:
            self.wf.newfilesname(taskIndex=taskIndex)
            self.wf.download_file(taskIndex= taskIndex)
        except:
            raise
    def start_app_import_flow(self):
        try:
            self.wbf.launch_MVBW()
            self.wbf.open_magicbox()
            self.wbf.magicbox_C_dick()
            self.wbf.magicbox_fileConvert_folder()
            self.wbf.magicbox_download_folder()
            self.wbf.import_file()
            self.wbf.select_all_page()
            self.wbf.landscape_image()
            self.wbf.wait_importing()
        except:
            if self.wbf.import_error():
                self.wf.add_error_file()
            raise
    def start_app_save_flow(self):
        try:
            self.wbf.open_page_management()
            self.wbf.delete_first_page()
            self.wbf.confirm_delete()
            self.wbf.wait_deleting()
            self.wbf.open_file_management()
            self.wbf.save_as_file()
            self.wbf.filemanager_C_disk()
            self.wbf.filemanager_fileConvert_folder()
            self.wbf.filemanager_convert_folder()
            self.wbf.save_olf_file()
        except:
            raise
    def start_web_upload_flow(self, taskIndex):
        try:
            self.wf.upload_file(taskIndex= taskIndex)
        except:
            raise
    def finish_task(self):        
        self.wf.fc.delete_all_files("./Download_File/")
        self.wf.fc.delete_all_files("./Convert_File/")
        self.wbf.finish_close_app()
        self.wf.finish_close_web()
        

class StartFileConversion:
    def __init__(self):
        self.currentPage = 1
    def test_(self):
        self.test = TestFileConversion()
        isNextPage = True
        self.test.wf.enter_webpage("https://worker.stage.myviewboard.cloud/", "DCC", "DCC")
        time.sleep(2)
        while isNextPage:
            pageList = []
            for i in range(len(self.test.wf.element.GetAllTasks)):
                print(i)
                try:
                    self.test.start_web_download_flow(i)
                    self.test.start_app_import_flow()
                    self.test.start_app_save_flow()
                    self.test.start_web_upload_flow(i)
                    self.test.wf.fc.delete_all_files("./Download_File/")
                    self.test.wf.fc.delete_all_files("./Convert_File/")
                    raise
                except:
                    self.test.wf.fc.delete_all_files("./Download_File/")
                    self.test.wf.fc.delete_all_files("./Convert_File/")
                    self.test.wbf.finish_close_app()
                    continue
            for i in range(len(self.test.wf.element.pages)):
                pageList.append(self.test.wf.element.pages[i].text)
            if str(self.currentPage + 1) in pageList:
                self.currentPage += 1
                self.test.wf.turn_page()
            else:
                isNextPage = False
                self.test.finish_task()


class TestApporveFileConversion:
    def __init__(self):
        self.wf = Web_Flow()
        self.failFiles = GetFiles("./Failed_File/failed_files.txt").Files
        
class ApproveFileConversion:
    def __init__(self, totalPage):
        self.test = TestApporveFileConversion()
        self.current_page = 1
        self.totalpage = totalPage
        print(self.totalpage)
        self.test_2()
    def finish_task(self):        
        self.test.wf.finish_close_web()
    def test_2(self):
        isNextPage = True
        self.test.wf.enter_webpage("https://worker.stage.myviewboard.cloud/", "admin", "12345")
        while isNextPage:
            if self.current_page < self.totalpage:
                self.test.wf.element.GetAllTasks
                for i in range(len(self.test.wf.element.GetAllTasks)):
                    self.test.wf.newfilesname(taskIndex=i)
                    if self.test.wf.element.States(i) == "Review":
                        if self.test.wf.createTime+self.test.wf.fileName in self.test.failFiles:
                            self.test.wf.approve_icon(i)
                        else:
                            print("這個檔案在失敗的列表中")
                    else:
                        print(f"這個檔案狀態是 {self.test.wf.element.States(i)} ")
                self.test.wf.turn_page()
                self.current_page += 1
            else:
                break
        self.finish_task()

            

a = StartFileConversion()
a.test_()
ApproveFileConversion(totalPage=a.currentPage)

