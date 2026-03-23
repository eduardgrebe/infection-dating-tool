class ResultDownload(object):

    def __init__(self, results):

        self.headers = ['Subject', 'EP DDI', 'LP DDI', 'Interval Size', 'EDDI', 'Flag']
        self.content = []
        self.results = results
        self.prepare_content()

    def get_content(self):
        return self.content

    def get_headers(self):
        return self.headers

    def getattr_or_none(self, obj, attr):
        value = obj
        value = getattr(value, attr, None)

        return value

    def prepare_content(self):
        columns = ['subject_label', 'ep_ddi', 'lp_ddi', 'interval_size', 'eddi', 'flag']
        for result in self.results:
            row = [self.getattr_or_none(result, c) for c in columns]
            self.content.append(row)
