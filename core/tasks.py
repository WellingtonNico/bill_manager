import binascii
from celery import shared_task
from django.core.mail import EmailMessage


@shared_task(name='send_mail_task',limit=10,auto_retry_for=(Exception,),max_retries=5)
def send_mail_task(send_to:list, subject:str, text:str, files:dict=None):
    """
    recebe uma lista de emails de destino, o conteúdo em texto somente
    e um dicionário contendo os arquivos, o dicionário deve ter como chave
    o nome do arquivo e como valor o arquivo em objeto,
    no caso de o envio ser feito através do celery, em vez do objeto no dicionário
    será necessário enviar o caminho relativo do arquivo
    """
    mail = EmailMessage(subject=subject,body=text,to=send_to)

    if files:
        for fileName,file in files.items():
            if type(file) == str:
                mail.attach(fileName,binascii.a2b_base64(file))
            elif hasattr(file,'read'):
                mail.attach(fileName,file.read())
            else:
                raise Exception('O formato do arquivo deve ser str ou um objeto IOBase')
    mail.send()