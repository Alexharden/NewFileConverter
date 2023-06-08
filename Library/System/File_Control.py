import os, time
from EventLog.exception_handler import ExceptionHandler

class FileControl: #下載存檔檔案相關的
    def create_folder(self, folderName): #創建資料夾
        if not os.path.isdir(folderName):
            os.mkdir(folderName)

    def delete_all_files(self, path): #刪除資料
        for i in range(len(os.listdir(path))):
            os.remove(os.path.join(os.path.abspath(path)+"\\"+os.listdir(path)[i]))
            
    def file_wait(self, path, extension): #等待檔案下載
        start_time = time.time()
        while True:
            try: 
                if extension not in os.listdir(path)[0]:
                    if time.time() - start_time > 120:
                        ExceptionHandler(msg= f"Timeout! The {extension} type file format cannot be found.", exceptionLevel= "critical")
                        break
                else:
                    break
            except:
                continue
    def add_failed_file(self, fileName): #寫入出錯的檔案至txt檔案
        with open("./Failed_File/failed_files.txt", "a", encoding= "utf-8") as f:
            f.write(fileName+"\n")
    