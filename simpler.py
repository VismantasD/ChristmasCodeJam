import requests
import numpy as np
import StringIO
import base64

def stringifynp(x):
    output = StringIO.StringIO()
    np.save(output, x)
    output.seek(0)
    return base64.b64encode(output.read())


x = np.random.random((10,10,2, 3, 4))
payload = {
        'teamname': 'Happy Feet',
        'predictions': stringifynp(x)
        }
r = requests.post('http://localhost:5000/submit', json=payload)
print x
print r.text
