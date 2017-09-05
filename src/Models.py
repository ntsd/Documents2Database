import json


class Customer:
    def __init__(self, name, boundaries):
        self.name = name
        self.boundaries = boundaries
        self.po = []

    def addPO(self, po):
        self.po.append(po)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Boundary:
    def __init__(self, name, rectangle):
        self.name = name
        self.rectangle = rectangle


class PO:
    def __init__(self, name):
        self.name = name
        self.data = []

    def addData(self, data):
        self.data.append(data)


class Data:
    def __init__(self, name, text):
        self.name = name
        self.text = text
