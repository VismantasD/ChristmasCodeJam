import requests
import numpy as np
import StringIO
import base64

def stringifynp(x):
    output = StringIO.StringIO()
    np.save(output, x)
    output.seek(0)
    return base64.b64encode(output.read())

def submit(name, secret, predictions):
    payload = {
        'teamname': name,
        'secret': secret,
        'predictions': stringifynp(predictions)
        }
    r = requests.post('http://localhost:5000/submit', json=payload)
    return r.text



x = np.random.random((10,10,2, 3, 4))
print submit('Norns', 5781, x)
