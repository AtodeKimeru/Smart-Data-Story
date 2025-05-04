from mage_ai.data_preparation import Variable
import snowflake.connector
import boto3
import json
import gzip

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    """
    Load data from S3 to Snowflake
    """
    # Get Snowflake credentials from variables
    snowflake_account = Variable.get_variable('SNOWFLAKE_ACCOUNT')
    snowflake_user = Variable.get_variable('SNOWFLAKE_USER')
    snowflake_password = Variable.get_variable('SNOWFLAKE_PASSWORD')
    snowflake_database = Variable.get_variable('SNOWFLAKE_DATABASE')
    snowflake_schema = Variable.get_variable('SNOWFLAKE_SCHEMA')
    
    # Create Snowflake connection
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database,
        schema=snowflake_schema
    )
    
    # Create stage if it doesn't exist
    cursor = conn.cursor()
    stage_name = 'github_events_stage'
    cursor.execute(f"""
    CREATE STAGE IF NOT EXISTS {stage_name}
    URL = 's3://{data['s3_bucket']}/github_events/raw/'
    CREDENTIALS = (AWS_KEY_ID='{Variable.get_variable('AWS_ACCESS_KEY_ID')}'
                  AWS_SECRET_KEY='{Variable.get_variable('AWS_SECRET_ACCESS_KEY')}')
    FILE_FORMAT = (TYPE = 'JSON');
    """)
    
    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS github_events (
        event_id STRING,
        event_type STRING,
        actor VARIANT,
        repo VARIANT,
        payload VARIANT,
        created_at TIMESTAMP,
        raw_data VARIANT
    );
    """)
    
    # Copy data from stage to table
    copy_query = f"""
    COPY INTO github_events
    FROM @{stage_name}/{data['date']}/{data['date']}-{data['hour']}.json.gz
    FILE_FORMAT = (TYPE = 'JSON')
    ON_ERROR = 'CONTINUE';
    """
    cursor.execute(copy_query)
    
    # Get number of rows loaded
    result = cursor.fetchone()
    rows_loaded = result[0] if result else 0
    
    cursor.close()
    conn.close()
    
    return {
        'rows_loaded': rows_loaded,
        'date': data['date'],
        'hour': data['hour']
    }

@test
def test_output(output, *args) -> None:
    """
    Test if the output is valid
    """
    assert output is not None, 'The output is undefined'
    assert 'rows_loaded' in output, 'No rows_loaded count in output'
    assert output['rows_loaded'] >= 0, 'Invalid number of rows loaded'
