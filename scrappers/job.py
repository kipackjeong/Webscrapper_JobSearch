class Job(object):
    def __init__(self, title, company, location, salary, summary, date, apply_url=None):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.summary = summary
        self.date = date
        self.apply_url = apply_url
