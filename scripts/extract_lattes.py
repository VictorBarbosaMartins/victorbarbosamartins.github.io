import os
from bs4 import BeautifulSoup

def extract_members(html_file):
    if not os.path.exists(html_file):
        print(f"Erro: Arquivo {html_file} nao encontrado.")
        return

    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    sections = {
        "Doutorado": "Orientacoes-em-andamento-Doutorado",
        "Mestrado": "Orientacoes-em-andamento-Mestrado",
        "Iniciacao Cientifica": "Orientacoes-em-andamento-Iniciacao-Cientifica",
        "Doutorado (Concluido)": "Orientacoes-concluidas-Doutorado",
        "Mestrado (Concluido)": "Orientacoes-concluidas-Mestrado"
    }

    results = {}

    for label, div_id in sections.items():
        results[label] = []
        section_div = soup.find('div', {'id': div_id})
        if section_div:
            items = section_div.find_all('div', class_='artigo-completo')
            for item in items:
                results[label].append(item.get_text().strip())

    # Formata para Markdown
    md_output = "### Research Group Members\n\n"
    for category, members in results.items():
        if members:
            md_output += f"#### {category}\n"
            for m in members:
                md_output += f"* {m}\n"
            md_output += "\n"
    
    return md_output

if __name__ == "__main__":
    # O usuario deve salvar a pagina do Lattes como 'lattes.html' na mesma pasta
    print(extract_members('lattes.html'))
