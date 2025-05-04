from mage_ai.data_preparation import Variable
import subprocess
import os

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    """
    Run dbt transformations on loaded data
    """
    # Set DBT project directory
    dbt_project_dir = 'dbt'
    
    # Change to DBT project directory
    os.chdir(dbt_project_dir)
    
    # Run DBT models
    try:
        # Run dbt models
        result = subprocess.run(
            ['dbt', 'run'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            'success': True,
            'output': result.stdout,
            'date': data['date'],
            'hour': data['hour']
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': e.stderr,
            'date': data['date'],
            'hour': data['hour']
        }

@test
def test_output(output, *args) -> None:
    """
    Test if the output is valid
    """
    assert output is not None, 'The output is undefined'
    assert 'success' in output, 'No success status in output'
    if not output['success']:
        assert 'error' in output, 'Failed run but no error message provided'
