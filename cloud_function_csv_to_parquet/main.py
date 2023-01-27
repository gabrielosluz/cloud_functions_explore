import pandas as pd
from parametros.env_configs import EnvConfigs
from google.cloud import bigquery
from google.cloud import storage
import numpy as np
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

        logging.info('Arquivo : {}'.format(uri))

        env_configs = EnvConfigs()

        blob_path = file['name'].split("/")

        project = env_configs.get_gcp_project()
        bucket_destination = env_configs.get_bucket_destination()
        dataset = blob_path[0].replace('-', '_')
        table = blob_path[1]
        data_execucao_portfolio = blob_path[2]
        filename = blob_path[3]

        table_id = project + "." + dataset + "." + table

        logging.info('Interface : {}'.format(table))
        logging.info('DataExecucaoPortfolio : {}'.format(data_execucao_portfolio))

        bucket = file['bucket']
        file_path = file['name']
        time_created = file['timeCreated']


        logging.info('Carregando o arquivo "{}" no dataframe.'.format(uri))
        df = pd.read_csv(uri, lines=True)
        df_count = len(df.index)

        df = df.fillna(value=np.nan)

        df = df.replace('None', '')

        df["FilenameInput"] = uri



        path_destination = "gs://" + bucket_destination + "/" + dataset.replace('_', '-') + "/" + \
                           table + "/" + data_execucao_portfolio + "/" + filename + '.parquet.gzip'

        logging.info('Convertendo e salvando o arquivo "{}" no formato parquet em "{}".'.format(uri, path_destination))
        df.to_parquet(path_destination, compression='gzip')

        logging.info('Deletando o arquivo "{}".'.format(uri))

        logging.info('Registrando na tabela de controle.')
        current_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        rows_to_insert = [{u"NomeArquivo": uri, u"QuantidadeRegistro": df_count, u"OrigemBucket": bucket,
                           u"TimeCreated": time_created, u"LoadDatetime": current_date}]

        bq = bigquery.Client()
        bq.insert_rows_json('generali-datalake-dev.data_quality.controle', rows_to_insert)

    except FileNotFoundError:
        logging.error('Arquivo não encontrado "{}"'.format(uri))
        return {"status": "error", "details": "Arquivo " + uri + " não encontrado."}, 400

    except Exception as e:
        logging.exception(e)
        return {"status": "error", "details": str(type(e).__name__)}, 400

    logging.info('status : Success')
    return {"status": "success"}
