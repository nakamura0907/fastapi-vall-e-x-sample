from ..exceptions import ApplicationException

# 正規表現でDetectedTextを抽出することができなかった場合に発生する例外
class DetectedTextNotFoundException(ApplicationException):
    def 