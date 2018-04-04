import json

from logging import DEBUG, INFO, WARN, ERROR, CRITICAL
from logging import Formatter
from logging import LogRecord

from math import modf


LOG_LEVEL_MAP = {
    DEBUG: "DEBUG",
    INFO: "INFO",
    WARN: "WARNING",
    ERROR: "ERROR",
    CRITICAL: "CRITICAL",
}
"""ログレベル ログレベル番号とマッピングさせる"""


class SDLogFormatter(Formatter):
    """Stackdriver用の形式にログを整形するフォーマッタ

    ログフォーマット:
        {
          "timestamp": {
              "second": epoctime,
              "nanos: nanotime
          },
          "severity": L,
          "thread": threadname,
          "message": log message,
        }
    フィールド:
        timestamp        タイムスタンプ
        timestamp.second 秒
        timestamp.nanos  ナノ秒
        severity         ログレベル
        thread           スレッド名
        mesage           ログメッセージ
    """

    def __init__(self):
        Formatter.__init__(self)

    def format(self, record: LogRecord) -> str:
        # ログレベルの設定 不明なログレベルの場合は "?" で出力
        level = LOG_LEVEL_MAP[record.levelno] if record.levelno in LOG_LEVEL_MAP.keys() else "?"
        t = modf(record.created)
        msg = {
            "timestamp": {"second": t[1], "nanos": int(t[0] * 1e6)},
            "severity": level,
            "thread": record.process,
            "message": record.getMessage(),
        }
        return json.dumps(msg)
