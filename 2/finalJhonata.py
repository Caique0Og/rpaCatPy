import requests
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText

# 1. Busca piadas na API garantindo 10 piadas únicas
def buscar_piadas():
    piadas = {}
    while len(piadas) < 10:
        resposta = requests.get("https://api.chucknorris.io/jokes/random")
        if resposta.ok:
            dados = resposta.json()
            piadas[dados["id"]] = dados["value"]  # evita duplicatas pelo id
    return [{"id": k, "texto": v} for k, v in piadas.items()]

# 2. Salva no banco de dados
def salvar_no_banco(piadas):
    conexao = sqlite3.connect("piadas.db")
    cursor = conexao.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS piadas
                      (id TEXT PRIMARY KEY, texto TEXT)''')
    
    for p in piadas:
        cursor.execute("INSERT OR IGNORE INTO piadas VALUES (?, ?)", 
                      (p["id"], p["texto"]))
    
    conexao.commit()
    return conexao

# 3. Analisa as piadas
def analisar_piadas(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT texto FROM piadas")
    
    total_palavras = 0
    total_numeros = 0
    
    for (texto,) in cursor.fetchall():
        total_palavras += len(re.findall(r'\b\w+\b', texto))
        total_numeros += len(re.findall(r'\d+', texto))
    
    return total_palavras, total_numeros

# 4. Envia e-mail em texto simples
def enviar_email(assunto, mensagem):
    remetente = "cayqtoky@gmail.com"
    destinatario = "caique.diniz@aluno.faculdadeimpacta.com.br"
    senha = "cgpnnrvhzyksixol"  # Recomendo usar senha de app para Gmail
    
    msg = MIMEText(mensagem, 'plain', 'utf-8')
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)

# Execução principal
if __name__ == "__main__":
    # Busca e salva piadas
    piadas = buscar_piadas()
    banco = salvar_no_banco(piadas)
    
    # Analisa as piadas
    palavras, numeros = analisar_piadas(banco)
    resumo = f"Total de palavras: {palavras}\nTotal de números: {numeros}"
    
    # Envia relatório
    enviar_email("Relatório Chuck Norris", resumo)
    banco.close()
    print("Processo concluído!")
