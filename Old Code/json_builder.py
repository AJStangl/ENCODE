__author__ = 'AJ'
import json
import python_jsonschema_objects as pjs
class Notebook:

    def __init__(self, name, desc, tp):
        self.metadata = {"name": name, "description": desc, "restricted": False, "type": tp}

test = Notebook(name="test", desc="desc", tp="mixed")
# test = json.dumps(test)
print json.dumps(vars(test))

