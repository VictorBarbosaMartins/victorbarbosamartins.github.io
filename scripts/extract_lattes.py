import os
import re
from bs4 import BeautifulSoup

def extract_members(html_file):
    if not os.path.exists(html_file):
        return f"Erro: Arquivo {html_file} nao encontrado."

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(html_file, 'r', encoding='iso-8859-1') as f:
            content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    # Procura por secoes de orientacao
    # O Lattes organiza por titulos de secao (h1 ou h2) ou divs com IDs especificos
    
    mapping = {
        "Doutorado (Em andamento)": "Doutorado",
        "Mestrado (Em andamento)": "Mestrado",
        "Iniciação Científica (Em andamento)": "Iniciação científica",
        "Doutorado (Concluído)": "Orientações de doutorado concluídas",
        "Mestrado (Concluído)": "Orientações de mestrado concluídas",
        "Iniciação Científica (Concluído)": "Orientações de iniciação científica concluídas"
    }

    md_output = ""
    
    # Encontra todos os blocos de 'inst-item' ou 'artigo-completo'
    all_sections = soup.find_all(['div', 'h1', 'h2', 'h3'])
    
    results = {k: [] for k in mapping.keys()}
    
    current_label = None
    for element in all_sections:
        text = element.get_text().strip()
        
        # Identifica a secao
        for label, keyword in mapping.items():
            if keyword.lower() in text.lower():
                current_label = label
                break
        
        # Se estamos em uma secao, procura itens proximos
        if current_label and element.name in ['div'] and 'artigo-completo' in element.get('class', []):
            item_text = element.get_text().strip()
            # Limpeza do texto
            if '. ' in item_text[:5]:
                item_text = item_text.split('. ', 1)[1]
            results[current_label].append(item_text)

    found_any = False
    for label, members in results.items():
        if members:
            md_output += f"### {label}\n"
            for m in members:
                md_output += f"* {m}\n"
            md_output += "\n"
            found_any = True

    if not found_any:
        # Busca desesperada por IDs de div se a busca por texto falhou
        sections_ids = {
            "Doutorado (Em andamento)": "orientacoes-em-andamento-doutorado",
            "Mestrado (Em andamento)": "orientacoes-em-andamento-mestrado",
            "Iniciação Científica (Em andamento)": "orientacoes-em-andamento-iniciacao-cientifica",
            "Doutorado (Concluído)": "orientacoes-concluidas-doutorado",
            "Mestrado (Concluído)": "orientacoes-concluidas-mestrado",
        }
        for label, div_id in sections_ids.items():
            div = soup.find('div', id=div_id)
            if div:
                items = div.find_all('div', class_='artigo-completo')
                if items:
                    md_output += f"### {label}\n"
                    for it in items:
                        md_output += f"* {it.get_text().strip()}\n"
                    md_output += "\n"
                    found_any = True

    return md_output if found_any else "Nenhum membro encontrado automaticamente."

if __name__ == "__main__":
    print(extract_members('lattes.html'))
