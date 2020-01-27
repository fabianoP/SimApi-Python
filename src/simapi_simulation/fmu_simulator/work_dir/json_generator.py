import json


class JsonSerializer:

    def __init__(self, fmu_vars):
        self.fmu_vars = fmu_vars

    def to_json(self):
        return json.dumps(self.fmu_vars)

    def to_dict(self, var_dict):
        return json.loads(var_dict)

    def to_json_file(self, file, output):
        with file as json_file:
            json.dump(output, json_file)

        return json_file

