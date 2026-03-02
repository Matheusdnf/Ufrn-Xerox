
from io import BytesIO
import os
from PIL import Image
from pypdf import PdfWriter, PdfReader

#refatorar para criar tudo de uma vez, só precisando passar o ano e não o turno 
def criar_pastas(ano):
    #Pastas Principais
    pastas_principais= ["MANHÃ","TARDE","NOITE","RELATÓRIOS"]
    #Pastas dos meses
    meses = [
        "01-JANEIRO", "02-FEVEREIRO", "03-MARÇO", "04-ABRIL", "05-MAIO", "06-JUNHO",
        "07-JULHO", "08-AGOSTO", "09-SETEMBRO", "10-OUTUBRO", "11-NOVEMBRO", "12-DEZEMBRO",
    ]
    #Diretório raiz
    diretorio_raiz="CONTROLE DE COMPROVANTES"
       
    for pastas in pastas_principais:
        if os.path.exists(os.path.join(diretorio_raiz,pastas,ano)):
            print(f"O ano {ano} já existe! em {pastas}")
            continue
        else:
            print(f"{pastas} ainda não existe com o ano {ano}, criado")
            os.makedirs(os.path.join(diretorio_raiz,pastas,ano))
            print(f"Criado O ano {ano} para a pasta: {pastas}")

    input("Pressione Enter para continuar...")
    
    for pastas in pastas_principais:
        criar_meses = os.path.join(diretorio_raiz, pastas, ano)

        os.makedirs(criar_meses,exist_ok=True)
        for mes in meses:
            os.makedirs(os.path.join(criar_meses, mes), exist_ok=True)

    print("Estrutura Criada")
    input("Pressione Enter para continuar...")


def pasta_relatorio(ano,mes):
    pasta_destino = f"RELATÓRIOS/{ano}/{mes}"
    return pasta_destino

def juntar_pdfs(lista_de_pdfs,pasta_principal,pasta_destino,nome_arquivo,mensagem_final):
    writer = PdfWriter()
    #vare cada pdf e vai juntando em um único pdf
    for pdf in lista_de_pdfs:
        for page in pdf.pages:
            writer.add_page(page)
    nome_pdf_turno = os.path.join(pasta_principal,pasta_destino,nome_arquivo)
    with open(nome_pdf_turno, "wb") as f_out:
        writer.write(f_out)
        
    print(mensagem_final)
    input("Pressione Enter para continuar...")


def pegar_nome_diretorios(caminho):
    diretorios=[]
    for diretorio in os.listdir(caminho):
        caminho_completo = os.path.join(caminho, diretorio)
        if os.path.isdir(caminho_completo):
            diretorios.append(diretorio)
    return diretorios



def verifica_diretorio_turno(turnos, diretorios):
    #evita duplicidades no vetor
    encontrados = set()

    # quebra cada item de "turnos" em palavras individuais
    palavras_turnos = []
    for turno in turnos:
        palavras_turnos.extend(turno.lower().split())

    # percorre os diretórios e verifica se alguma palavra aparece no nome da pasta
    for diretorio in diretorios:
        nome_lower = diretorio.lower()
        for palavra in palavras_turnos:
            if palavra in nome_lower:
                encontrados.add(diretorio)

    return list(encontrados)


def juntar_pdfs_e_imagens_turnos(ano,mes):
    
    turnos = ["MANHÃ", "TARDE", "NOITE"]    
    
    pasta_principal="CONTROLE DE COMPROVANTES"

    diretorios=pegar_nome_diretorios(pasta_principal)


    vetor_turno=verifica_diretorio_turno(turnos,diretorios)
 
    # RELATÓRIOS/ANO/MÊS
    pasta_destino = pasta_relatorio(ano,mes)


    todos_arquivos_geral = []


    for turno in vetor_turno:
        diretorio_turno = os.path.join(pasta_principal,turno, ano, mes)
        arquivos_turno = []
        if os.path.exists(diretorio_turno):
            for pasta_atual, subpastas, arquivos in os.walk(diretorio_turno):
                for arquivo in arquivos:
                    caminho_completo = os.path.join(pasta_atual, arquivo)
                    arquivos_turno.append(caminho_completo)
        else:
            print(f"Pasta do turno não encontrada: {diretorio_turno}")
            input("Pressione Enter para continuar...")
            continue
        
        if arquivos_turno:
            pdfs_convertidos = []
            for arquivo in arquivos_turno:
                ext = os.path.splitext(arquivo)[1].lower()
               
            
                if ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
                    img = Image.open(arquivo).convert("RGB")
                    pdf_bytes = BytesIO()
                    img.save(pdf_bytes, format="PDF")
                    pdf_bytes.seek(0)
                    reader = PdfReader(pdf_bytes)
                    pdfs_convertidos.append(reader)

                elif ext == ".pdf":
                    reader = PdfReader(arquivo)
                    pdfs_convertidos.append(reader)

                else:
                    print(f"Arquivo ignorado: {arquivo}")
                    input("Pressione Enter para continuar...")

            mensagem_sucesso=f"PDF do turno '{turno}' criado com {len(pdfs_convertidos)} arquivos!"
            nome_arquivo = f"{ano}_{mes}_{turno}.pdf"
            juntar_pdfs(pdfs_convertidos,pasta_principal,pasta_destino,nome_arquivo,mensagem_sucesso)
        
            todos_arquivos_geral.extend(pdfs_convertidos)

    mensagem_sucesso=f"PDF geral criado com {len(todos_arquivos_geral)} arquivos!"
    nome_arquivo= f"{ano}_{mes}_todos_turnos.pdf"
    juntar_pdfs(todos_arquivos_geral,pasta_principal,pasta_destino,nome_arquivo,mensagem_sucesso)
    input("Pressione Enter para continuar...")




