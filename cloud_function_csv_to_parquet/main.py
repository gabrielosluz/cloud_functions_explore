import pandas as pd
from parametros.env_configs import EnvConfigs
from google.cloud import bigquery
from google.cloud import storage
import numpy as np
import datetime
from datetime import datetime
import logging
import google.cloud.logging

logging_client = google.cloud.logging.Client()
logging_client.get_default_handler()
logging_client.setup_logging()


def main(event, context):

    uri = ""

    try:

        file = event

        uri = 'gs://' + file['bucket'] + "/" + file['name']

        logging.info('Processando o arquivo "{}".'.format(uri))

        env_configs = EnvConfigs()

        project = env_configs.get_gcp_project()
        bucket_destination = env_configs.get_bucket_destination()
        bucket_source = env_configs.get_bucket_source()

        bucket = file['bucket']
        file_path = file['name']

        logging.info('Carregando o arquivo "{}" no dataframe.'.format(uri))
        df = pd.read_csv(uri)

        df["File_Source"] = file['name']
        df["Ingestion_Date"] = pd.Timestamp.today().strftime('%Y-%m-%d')

        logging.info('Carregando arquivo: "{}" no bucket historico.'.format(file['name']))

        path_destination = "gs://" + bucket_destination + "/" + str(datetime.now().date()) + "/" + file_path + '.parquet.gzip'

        logging.info('Convertendo e salvando o arquivo "{}" no formato parquet em "{}".'.format(uri, path_destination))

        df.to_parquet(path_destination, compression='gzip')



    except Exception as e:
        logging.exception(e)
        return {"status": "error", "details": str(type(e).__name__)}, 400

    logging.info('status : success')
    return {"status": "success"}



