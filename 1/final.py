import requests
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


def coletar_dados_catapi(api_key="DEMO-API-KEY"):
    """
    Justificativa da escolha:
    A The Cat API foi escolhida por ser gratuita, aberta, fácil de usar e fornecer dados ricos sobre gatos, incluindo imagens, raças e fatos. Isso permite demonstração de automação, integração com API REST e manipulação de dados reais e divertidos, tornando o projeto didático e interessante.
    """
    url = "https://api.thecatapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=5"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    dados = response.json()
    
    dados_estruturados = []
    for item in dados:
        if item.get("breeds"):
            breed = item["breeds"][0]
            dados_estruturados.append({
                "id": item["id"],
                "url": item["url"],
                "breed": breed.get("name", ""),
                "origin": breed.get("origin", ""),
                "description": breed.get("description", "")
            })
    return dados_estruturados


def criar_banco_e_tabela():
    conn = sqlite3.connect("projeto_rpa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gatos (
            id TEXT PRIMARY KEY,
            url TEXT,
            breed TEXT,
            origin TEXT,
            description TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_processados (
            id TEXT PRIMARY KEY,
            breed TEXT,
            origin TEXT,
            tem_palavra_cat INTEGER,
            qtd_palavras_desc INTEGER
        )
    """)
    conn.commit()
    conn.close()

def inserir_gatos(dados):
    conn = sqlite3.connect("projeto_rpa.db")
    cursor = conn.cursor()
    for d in dados:
        cursor.execute(
            "INSERT OR IGNORE INTO gatos VALUES (?, ?, ?, ?, ?)",
            (d["id"], d["url"], d["breed"], d["origin"], d["description"])
        )
    conn.commit()
    conn.close()

# 3. Processamento com re
def processar_gatos():
    conn = sqlite3.connect("projeto_rpa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, breed, origin, description FROM gatos")
    for row in cursor.fetchall():
        id_, breed, origin, desc = row
       
        tem_cat = 1 if re.search(r"\bcat\b", desc, re.IGNORECASE) else 0
      
        qtd_palavras = len(re.findall(r"\b\w+\b", desc))
        cursor.execute(
            "INSERT OR REPLACE INTO dados_processados VALUES (?, ?, ?, ?, ?)",
            (id_, breed, origin, tem_cat, qtd_palavras)
        )
    conn.commit()
    conn.close()


def enviar_email(relatorio):
    remetente = "cayqtoky@gmail.com"
    destinatario = "caique.diniz@aluno.faculdadeimpacta.com.br"
    senha = "cgpnnrvhzyksixol"
    msg = MIMEText(relatorio, 'plain', 'utf-8')
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"Relatório The Cat API - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)

def gerar_relatorio():
    conn = sqlite3.connect("projeto_rpa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gatos")
    gatos = cursor.fetchall()
    cursor.execute("SELECT * FROM dados_processados")
    processados = cursor.fetchall()
    conn.close()

    relatorio = "Relatório The Cat API\n"
    relatorio += "====================\n"
    relatorio += f"Total de gatos coletados: {len(gatos)}\n\n"
    relatorio += "Justificativa da API:\nA The Cat API foi escolhida por ser gratuita, aberta, fácil de usar e fornecer dados ricos sobre gatos, incluindo imagens, raças e fatos. Isso permite demonstração de automação, integração com API REST e manipulação de dados reais e divertidos.\n\n"
    relatorio += "Resumo dos dados coletados e processados:\n"

    for g, p in zip(gatos, processados):
        relatorio += (
            f"- ID: {g[0]}\n"
            f"  Raça: {g[2]}\n"
            f"  Origem: {g[3]}\n"
            f"  Descrição: {g[4][:60]}...\n"
            f"  Contém 'cat' na descrição: {'Sim' if p[3] else 'Não'}\n"
            f"  Nº de palavras na descrição: {p[4]}\n"
        )
    return relatorio


if __name__ == "__main__":
    print("Coletando dados da The Cat API...")
    dados = coletar_dados_catapi()
    criar_banco_e_tabela()
    inserir_gatos(dados)
    processar_gatos()
    relatorio = gerar_relatorio()
    print(relatorio)
    enviar_email(relatorio)  
