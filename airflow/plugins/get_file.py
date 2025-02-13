import requests
from io import StringIO
import pandas as pd
import os 

now = pd.Timestamp.now()
year = now.year
month = now.month
day = now.day


def get_data():
    url = 'https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD'

    response = requests.get(url)

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        data11= pd.read_csv(csv_data)
        print(data11.head())


        # Create the directory path if it doesn't exist
        data_dir = '/opt/airflow/data'
        print(data_dir)
        os.makedirs(data_dir, exist_ok=True)
        print(os.makedirs(data_dir, exist_ok=True))
        # Save the cleaned data to a new file
        data11.to_csv(f'{data_dir}/xrate.csv', index=False)


