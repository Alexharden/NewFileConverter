import os, time
from EventLog.exception_handler import ExceptionHandler

class FileControl: #下載存檔檔案相關的
    def create_folder(self, folderName): #創建資料夾
        if not os.path.isdir(folderName):
            os.mkdir(folderName)

    def delete_all_files(self, path): #刪除資料
        try:
            while len(os.listdir(path)) != 0:
                for i in range(len(os.listdir(path))):
                    os.remove(os.path.join(os.path.abspath(path)+"\\"+os.listdir(path)[i]))
        except:
            print("此資料夾為空")
            
    def file_wait(self, path, extension): #等待檔案下載
        start_time = time.time()
        while True:
            try:
                downloadExt = os.listdir(path)[0] 
            except:
                downloadExt = ""
            if path != "./Download_File/":
                try:
                    if time.time() - start_time > 120 and extension not in downloadExt:
                        ExceptionHandler(msg= f"時間到 {extension} 超過時間囉.", exceptionLevel= "critical")
                        raise
                    elif time.time() - start_time < 120 and extension in downloadExt:
                            break
                    else:
                        continue
                except:
                    raise
            else:
                if extension in downloadExt:
                    ExceptionHandler(msg= f"{extension} 已被存於 {path}路徑中.", exceptionLevel= "info")
                    break
                else:
                    continue
        
    def add_failed_file(self, fileName): #寫入出錯的檔案至txt檔案
        with open("./Failed_File/failed_files.txt", "a", encoding= "utf-8") as f:
            f.write(fileName+"\n")
    