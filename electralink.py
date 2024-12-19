import requests
import json
import time

import pandas as pd
import numpy as np



from io import StringIO

postcode = 'rg415hu'

def sites(mpan, postcode, attempts=1):
	
	response_type = 'csv'

	if mpan != False:
		api_url = f"https://api.electralink.co.uk/v1/encmpaneacfulltpr?mpan={mpan}"
	else:	
		api_url = f'https://api.electralink.co.uk/v1/encmpanpostcodesearch?postcode={postcode}'
	headers = { 'api-key': 'uPJbptyc5hZmssT8EHWINKBfH',
		'api-password': 'uHSSWDBXvJpKNYcV',
		'response-type': response_type
	}
	
	df = pd.DataFrame()
	
	received_data, attempt = False, 0
	while received_data == False and attempt < attempts:
	
		try:
			r = requests.get(api_url, headers=headers)
	
			df = pd.read_csv(StringIO(r.text), header=None).T.set_index(0).T

			
			received_data= True
			break
		
		except:
			pass
		
		attempt += 1
		time.sleep(1)
	
	return df

df = sites(False, postcode)

output = pd.DataFrame()
for m in df.mpan:
	temp = sites(m,'')
	output = pd.concat([output, temp])
output.to_csv(f'{postcode}.csv', index = False)
