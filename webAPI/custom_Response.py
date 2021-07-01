
class ResponseInfo(object):
    def __init__(self, user=None, **args):
        self.response = {
            "msg": args.get('msg', 'ดึงข้อมูลสำเร็จ'),
            "data": args.get('data', []),
        }