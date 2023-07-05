# from Flow.Conversion_Flow import Web_Flow
# from Flow.Conversion_Flow import Whiteboard_Flow
# from Element.Elements import Elements_FileConversion
# from Flow.Conversion_Flow import GetFiles
# from EventLog.exception_handler import ExceptionHandler
# import os, psutil
# 本來配合以下 有使用到的 只有這個from File_Convert_Steps import  StartFileConversion, ApproveFileConversion

from File_Convert_Steps import  StartFileConversion, ApproveFileConversion
import time, os
from EventLog.exception_handler import ExceptionHandler

startTime = time.time()
a = StartFileConversion()
a.convert_flow()
ApproveFileConversion(totalPage=a.currentPage).approve_flow()
ExceptionHandler(msg= f"本次任務共花了 {round(time.time()-startTime, 1)} 秒", exceptionLevel= "info")
os.system("TASKKILL /F /IM FileConverter.exe /T")









#------------------------以下為harden
# a = StartFileConversion()
# a.test_()
# ApproveFileConversion(totalPage=a.currentPage).test_2()