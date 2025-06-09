import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_relatorio_email(remetente, senha, destinatario, resumo):
    # Cria a mensagem do e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = "Relatório Automático - Dados Processados"

    # Corpo do e-mail formatado em HTML com suporte a UTF-8
    corpo = f"""
    <html>
      <body>
        <p>Olá,</p>
        <p>Segue abaixo o resumo dos dados coletados e processados:</p>
        <pre style="font-family: monospace; background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
{resumo}
        </pre>
        <p>Atenciosamente,<br>Sistema Automatizado</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(corpo, 'html', 'utf-8'))

    # Configura o servidor SMTP (exemplo para Gmail)
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(msg)
        servidor.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)

# Exemplo de uso
if __name__ == "__main__":
    remetente = "cayqtoky@gmail.com"
    senha = "cgpnnrvhzyksixol"  # Recomendo usar senha de app para Gmail
    destinatario = "cayqtoky@gmail.com"
    resumo = "Total de piadas coletadas: 10\nMédia de palavras por piada: 15\nMédia de números por piada: 0"

    enviar_relatorio_email(remetente, senha, destinatario, resumo)


# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def enviar_email():  
#     corpo_email = """
#     <p>Parágrafo1 com acentuação: Olá, tudo bem?</p>
#     <p>Parágrafo2 com caracteres especiais: ç ã é</p>
#     """

#     msg = MIMEMultipart()
#     msg['Subject'] = "Assunto"
#     msg['From'] = 'cayqtoky@gmail.com'
#     msg['To'] = 'cayqtoky@gmail.com'

#     # MIMEText com charset UTF-8 e conteúdo HTML
#     msg.attach(MIMEText(corpo_email, 'html', 'utf-8'))

#     password = 'cgpnnrvhzyksixol' 

#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     s.starttls()
#     s.login(msg['From'], password)
#     s.send_message(msg)
#     s.quit()
#     print('Email enviado')

# enviar_email()

