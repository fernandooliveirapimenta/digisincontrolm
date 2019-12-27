import boto3
import json
from time import sleep

job1 = 'awsCliJob1'
fila_job1 = 'sensoriamento-mobile-batch-zarc-QUEUE-DEV'
def_job1 = 'sensoriamento-mobile-batch-zarc-JOBDEF-DEV'

job2 = 'awsCliJob2'
fila_job2 = 'sensoriamento-mobile-batch-zarc-QUEUE-DEV'
def_job2 = 'sensoriamento-mobile-batch-zarc-JOBDEF-DEV'

profile_name = 'dev'

sucesso = 'SUCCE'
falha = 'FAIL'

bucket = 'dev-brasilseg-ged'

boto3.setup_default_session(profile_name=profile_name)
client = boto3.client('batch')


def is_pode_continuar(jobId):
    continuar = True
    while continuar:
        sleep(5)
        job1Desc = client.describe_jobs(
            jobs=[jobId]
        )
        status = job1Desc['jobs'][0]['status']
        print(f'Status job: {jobId} = {status}')
        if sucesso in status:
            continuar = False
        if falha in status:
            raise Exception(f'Falha no job: {jobId}')


def start_aws_batch_sync(jobName, fila_job, def_job,):
    print(f'Startando aws batch {def_job}')
    responseJob1 = client.submit_job(
        jobName=jobName,
        jobQueue=fila_job,
        jobDefinition=def_job
    )
    jobId = responseJob1['jobId']
    is_pode_continuar(jobId)
    print(f'deu certo {jobName}: {jobId}')


if __name__ == '__main__':
    start_aws_batch_sync(job1, fila_job1, def_job1)

    #  todo implementar papel do datasync
    start_aws_batch_sync(job2, fila_job2, def_job2)
