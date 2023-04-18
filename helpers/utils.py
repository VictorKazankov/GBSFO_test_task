import json
import random
import string

random_string = (''.join(random.choices(string.ascii_lowercase, k=5)))

def json_to_python_object(response_result):
    return json.loads(response_result.text)
