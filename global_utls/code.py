

SUCCESS = 200

PARAM_NOT_ACCEPTED = 400
NOT_LOGIN = 401
PARAM_REQUIRED = 402
FORBIDDEN = 403
NOT_FOUND = 404

EMPTY_DATA = 2002

ARTICLE_ID_INVAILD = 2002

UID_MISS = 1001
USERNAME_MISS = 1002
PASSWORD_EMPTY = 1003
PASSWORD_NOT_MATCH = 1004
EMAIL_INVALID = 1005
USER_Be_FOLLOWED = 1006
USER_BeNot_FOLLOWED = 1007
USER_SESSION_MISS = 1008
USER_SESSION_ERROR = 1009
#UID_ERROR = 1002
COMMENT_ID_INVALID = 3001
COMMENT_EMPTY = 3002

ARTICLE_ID_INVAILD = 3003

CHILD_COMMENT_NOT_EXIST = 3005

MESSAGE_NOT_EXIST = 3010
#ARTICLE_OR_USER_MUST_ONE = 3004
NOT_EMPTY_ERROR = 5001
METHOD_ERROR = 4001
MISS_PARAM = 4002
VALUE_ERROR = 4003
IMAGE_FORMAT_ERROR = 4004


class Item(object):

    def succss_data(self, data = {}):
        _info = {}
        _info['msg'] = u'success'
        _info['code'] = SUCCESS
        _info['data'] = data
        return _info

    @classmethod
    def error_info(cls, message, code):
        _info = {}
        _info['msg'] = message
        _info['code'] = code
        return _info

class Results(object):

    def __init__(self, page=1, nums=1, total=1):
        self.page = page
        self.nums = nums
        self.total = total

    def succss_result(self, data = []):
        _info = {}
        _info['msg'] = u'success'
        _info['code'] = SUCCESS
        _info['data'] = {
            'page': self.page,
            'numpages': self.nums,
            'sum': self.total,
            'results': data,
            }
        return _info

    @classmethod
    def error_info(cls, message, code):
        _info = {}
        _info['msg'] = message
        _info['code'] = code
        return _info
