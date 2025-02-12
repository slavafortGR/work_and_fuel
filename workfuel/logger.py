import logging
import os


log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


log_file = os.path.join(log_dir, "error.log")
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.ERROR)


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
