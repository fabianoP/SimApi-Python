import json


class JsonSerializer:

    @staticmethod
    def to_json(var_dict):
        return json.dumps(var_dict)

    @staticmethod
    def to_dict(var_json):
        return json.loads(var_json)

    @staticmethod
    def to_json_file(file, output):
        with file as json_file:
            json.dump(output, json_file)

        return json_file

