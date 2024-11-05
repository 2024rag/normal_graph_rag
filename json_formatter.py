import logging
import json

class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
    def format(self, record):
        # 创建一个字典，包括想要的所有日志信息
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno
        }
        # 使用json.dumps将字典转换为JSON格式字符串
        return json.dumps(log_record, ensure_ascii=False)

logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("./pdf.log", mode='a') #to save to file
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)