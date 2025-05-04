import boto3
from mage_ai.data_preparation import Variable

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    """
    Upload downloaded GitHub Archive file to S3
    """
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=Variable.get_variable('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=Variable.get_variable('AWS_SECRET_ACCESS_KEY'),
        region_name=Variable.get_variable('AWS_REGION', 'us-east-1')
    )
    
    # Get file information from previous block
    local_file = data['filepath']
    date = data['date']
    hour = data['hour']
    
    # Upload file to S3
    bucket_name = Variable.get_variable('S3_BUCKET_NAME')
    s3_key = f'github_events/raw/{date}/{date}-{hour}.json.gz'
    
    s3_client.upload_file(local_file, bucket_name, s3_key)
    
    return {
        's3_bucket': bucket_name,
        's3_key': s3_key,
        'date': date,
        'hour': hour
    }

@test
def test_output(output, *args) -> None:
    """
    Test if the output is valid
    """
    assert output is not None, 'The output is undefined'
    assert 's3_bucket' in output, 'No S3 bucket specified in output'
    assert 's3_key' in output, 'No S3 key specified in output'
