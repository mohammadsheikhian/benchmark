class StatusAnalize:
    success_status = 0
    failed_status = 0


class R:

    def __init__(self, index=None, url=None, method_name=None, form=None,
                 headers=None):

        self.index = index
        self.url = url
        self.method_name = method_name
        self.form = form
        self.headers = headers

