import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email(report: str, png_images: list):
    """
    Envia um e-mail com um relatório meteorológico e imagens em anexo.

    Esta função compõe e envia um e-mail com um texto de relatório no corpo e múltiplas
    imagens PNG anexadas. O remetente, destinatário e senha do aplicativo devem estar
    definidos via variáveis de ambiente: EMAIL_REMETENTE, EMAIL_DESTINATARIO e SENHA_APP.

    Parâmetros:
    ----------
    report : str
        Texto do relatório a ser enviado no corpo do e-mail.

    png_images : list
        Lista de caminhos para arquivos PNG que serão anexados ao e-mail.

    Exceções:
    --------
    Certifique-se de que as variáveis de ambiente estejam corretamente configuradas e que
    os arquivos informados existam, caso contrário ocorrerão erros durante a execução.

    Exemplo de uso:
    --------------
    send_email(report="Resumo meteorológico do dia", png_images=["grafico1.png", "grafico2.png"])
    """
    msg = EmailMessage()
    msg['Subject'] = '📊 Relatório Meteorológico Diário'
    msg['From'] = os.getenv("EMAIL_REMETENTE")
    msg['To'] = os.getenv("EMAIL_DESTINATARIO")

    msg.set_content(report)

    for image in png_images:
        with open(image, 'rb') as f:
            img_data = f.read()
            archive_name = os.path.basename(image)
            msg.add_attachment(img_data, maintype='image', subtype='png', filename=archive_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_REMETENTE"), os.getenv("SENHA_APP"))
        smtp.send_message(msg)