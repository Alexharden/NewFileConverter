from EventLog.exception_handler import ExceptionHandler

class RetryMechanism: #重試
    def __init__(self, function, *args):
        self.retryCount = 0
        self.retry(function, *args)

    def retry(self, function, *args):
        while self.retryCount < 3:
            try:
                return function(*args)
            except:
                self.retryCount += 1
                if self.retryCount < 3:
                    ExceptionHandler(msg = f"出現問題，重試{self.retryCount}次", exceptionLevel= "error")
                else:
                    ExceptionHandler(msg= f"重試{self.retryCount}次仍出現問題，結束此任務", exceptionLevel= "critical")
                    break