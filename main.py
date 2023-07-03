# from Flow.Conversion_Flow import Web_Flow
# from Flow.Conversion_Flow import Whiteboard_Flow
# from Element.Elements import Elements_FileConversion
# from Flow.Conversion_Flow import GetFiles
# from EventLog.exception_handler import ExceptionHandler
# import os, psutil
from test import  StartFileConversion, ApproveFileConversion


a = StartFileConversion()
a.test_()
ApproveFileConversion(totalPage=a.currentPage)