import numpy as np
import pandas as pd
import requests
import json

url = "https://api.covid19india.org/raw_data.json"
JSONContent = requests.get(url).json()
content = json.dumps(JSONContent, indent=4, sort_keys=True)
print(content)
df = pd.read_json(content)
df.to_csv("./raw_data.csv")
