import os
import requests
from datetime import datetime, timedelta
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Descarga archivos de GH Archive desde una fecha de inicio hasta una final.
    Parámetros opcionales: start_date, end_date, download_dir
    """
    start = kwargs.get('start_date', '2025-01-01')
    end = kwargs.get('end_date', '2025-01-03')
    download_dir = kwargs.get('download_dir', 'gharchive_data')

    os.makedirs(download_dir, exist_ok=True)
    current = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    downloaded_files = []

    while current <= end_date:
        for hour in range(24):
            timestamp = current.strftime('%Y-%m-%d') + f'-{hour}'
            url = f'https://data.gharchive.org/{timestamp}.json.gz'
            local_path = os.path.join(download_dir, f'{timestamp}.json.gz')
            if not os.path.exists(local_path):
                print(f'Descargando {url}')
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    downloaded_files.append(local_path)
                else:
                    print(f'Error al descargar {url}: {response.status_code}')
        current += timedelta(days=1)

    return {
        "start_date": start,
        "end_date": end,
        "download_dir": download_dir,
        "files_downloaded": downloaded_files
    }


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert isinstance(output, dict), 'El output debe ser un diccionario'
    assert 'files_downloaded' in output, 'No se encuentra la clave files_downloaded'


# if __name__ == "__main__":
#     resultado = load_data_from_api()
#     print(resultado)
