import requests
from datetime import datetime, timedelta
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data(*args, **kwargs):
    """
    Downloads GitHub Archive data files for a specific date
    """
    # Get yesterday's date as GitHub Archive data is typically available the next day
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    hour = '00'  # Start with first hour of the day
    
    # Create data directory if it doesn't exist
    data_dir = 'data/raw'
    os.makedirs(data_dir, exist_ok=True)
    
    # Download file for specific hour
    filename = f'{yesterday}-{hour}.json.gz'
    url = f'https://data.gharchive.org/{yesterday}-{hour}.json.gz'
    
    local_file = os.path.join(data_dir, filename)
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_file, 'wb') as f:
            f.write(response.raw.read())
            
    return {
        'filepath': local_file,
        'date': yesterday,
        'hour': hour
    }

@test
def test_output(output, *args) -> None:
    """
    Test if the output is valid
    """
    assert output is not None, 'The output is undefined'
    assert 'filepath' in output, 'No filepath in output'
    assert os.path.exists(output['filepath']), 'Downloaded file does not exist'
