from mage_ai.io.file import FileIO

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import boto3
from pathlib import Path

@data_exporter
def export_data_to_file(**kwargs) -> None:
    """
    Exporta el DataFrame a un archivo CSV y luego sube todos los archivos .json.gz del directorio especificado a S3.
    Parámetros esperados en kwargs:
        - bucket_name: nombre del bucket S3
        - directory: directorio local con archivos .json.gz
        - s3_prefix: prefijo opcional en S3
        - endpoint_url, access_key, secret_key: opcionales para MinIO u otros S3 compatibles
    """

    # Parámetros para S3
    bucket_name = kwargs.get('bucket_name')
    directory = kwargs.get('directory')
    s3_prefix = kwargs.get('s3_prefix', '')
    endpoint_url = kwargs.get('endpoint_url')
    access_key = kwargs.get('access_key')
    secret_key = kwargs.get('secret_key')

    if bucket_name and directory:
        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        for file_path in Path(directory).rglob("*.json.gz"):
            s3_key = f"{s3_prefix}/{file_path.name}" if s3_prefix else file_path.name
            s3.upload_file(str(file_path), bucket_name, s3_key)
            print(f'Se subió {file_path} a s3://{bucket_name}/{s3_key}')
    else:
        print("Parámetros 'bucket_name' y 'directory' son requeridos para la subida a S3.")
        
if __name__ == "__main__":
    # Example of manual execution with required parameters
    test_df = DataFrame()  # Replace with your actual DataFrame if needed
    export_data_to_file(
        bucket_name='your-bucket-name',
        directory='path/to/your/local/directory',
        s3_prefix='optional/prefix',  # Optional
        endpoint_url='your-endpoint-url',  # Optional, for MinIO or other S3-compatible services
        access_key='your-access-key',  # Optional
        secret_key='your-secret-key'  # Optional
    )
