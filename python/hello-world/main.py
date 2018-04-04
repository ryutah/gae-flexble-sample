import os
import sys

from sdlog_formatter import SDLogFormatter

from flask import Flask
from logging import DEBUG, getLogger, StreamHandler
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

logger = getLogger(__name__)

if "LOG_FILE_PATH" in os.environ.keys():
    # ログ出力先が設定されている場合はログファイルへ出力
    # ローテーション設定は感覚なので最適ではないと思う。
    handler = RotatingFileHandler(
        filename=os.environ["LOG_FILE_PATH"],
        backupCount=1, encoding="utf8", maxBytes=(1 << 10 * 2),
    )
else:
    handler = StreamHandler(sys.stdout)

handler.setFormatter(SDLogFormatter())
logger.addHandler(handler)
logger.setLevel(DEBUG)


@app.route("/")
def hello():
    """Return friendly HTTP greeting."""
    return "Hello World!"


@app.route("/logsample")
def log_sample():
    """Log level examples"""
    logger.debug("This is debug")
    logger.info("This is info")
    logger.warn("This is warn")
    logger.error("This is error")
    logger.critical("This is critical")
    return "Output loggs"


if __name__ == "__main__":
    # Call only locally
    app.run(host="127.0.0.1", port=8080, debug=False)
