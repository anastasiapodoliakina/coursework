import requests
from bs4 import BeautifulSoup as bs
import os
import pdfplumber
import pandas as pd
import re
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL_TEMPLATE = "https://results.isu.org/results/season2122/owg2022/"
DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def download_pdf(pdf_link):
    pdf_url = os.path.join(URL_TEMPLATE, pdf_link) if not pdf_link.startswith("http") else pdf_link
    pdf_filename = os.path.join(DATA_FOLDER, pdf_url.split("/")[-1])
    
    if "FSKXTEAM--------------------------_EntryListbyEvent.pdf" in pdf_filename:
        return
    
    if not os.path.exists(pdf_filename):
        try:
            with requests.get(pdf_url) as pdf_file:
                pdf_file.raise_for_status()
                with open(pdf_filename, 'wb') as f:
                    f.write(pdf_file.content)
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при скачивании {pdf_url}: {e}")

try:
    r = requests.get(URL_TEMPLATE)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    logging.error(f"Ошибка при получении страницы: {e}")
    exit()

soup = bs(r.text, 'html.parser')
pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
pdf_links = list(set(pdf_links))

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(download_pdf, pdf_links)

pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.pdf')]

skaters_data = {}
executed_elements = {}
program_components = {}

def parse_filename(filename):
    filename_upper = filename.upper()

    if "FNL" in filename_upper and ("FSKXICEDANCE" in filename_upper or "DC" in filename_upper):
        segment = "Free Dance"
    elif "QUAL" in filename_upper and ("FSKXICEDANCE" in filename_upper or "DC" in filename_upper):
        segment = "Rhythm Dance"
    elif "FNL" in filename_upper:
        segment = "Free Skating"
    elif "QUAL" in filename_upper:
        segment = "Short Program"
    else:
        segment = "Unknown"

    if "FSKMSINGLES" in filename_upper:
        category = "Men Single Skating"
    elif "FSKWSINGLES" in filename_upper:
        category = "Women Single Skating"
    elif "FSKXICEDANCE" in filename_upper:
        category = "Ice Dance"
    elif "FSKXPAIRS" in filename_upper:
        category = "Pair Skating"
    elif "FSKXTEAM" in filename_upper:
        if "MN" in filename_upper:
            category = "Team Event - Men Single Skating"
        elif "LD" in filename_upper:
            category = "Team Event - Women Single Skating"
        elif "PR" in filename_upper:
            category = "Team Event - Pair Skating"
        elif "DC" in filename_upper:
            category = "Team Event - Ice Dance"
        else:
            category = "Team Event - Unknown"
    else:
        category = "Unknown"

    return segment, category

skater_pattern = re.compile(
    r'(\d+)\s+([A-Za-zÀ-ÿ\-\.\']+(?:\s+[A-Za-zÀ-ÿ\-\.\']+)*)(?:\s*/\s*([A-Za-zÀ-ÿ\-\.\']+(?:\s+[A-Za-zÀ-ÿ\-\.\']+)*))?\s+([A-Z]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.-]+)'
)

element_pattern = re.compile(
    r'(\d+)\s+([A-Za-z0-9+!*e<>]+)\s*([xq<!*e>]*)?\s+([\d.]+)\s*(x)?\s+([\d.-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+([\d.]+)'
)

component_pattern = re.compile(
    r'([A-Za-z\s]+?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)'
)

for pdf_file in pdf_files:
    pdf_path = os.path.join(DATA_FOLDER, pdf_file)
    segment, category = parse_filename(pdf_file)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            
            if not text:
                continue

            text = ' '.join(text.split())
            text = text.replace('\xa0', ' ').replace('\t', ' ')

            skater_blocks = re.split(r'(?=\d+\s+[A-Za-zÀ-ÿ\-\.\']+(?:\s+[A-Za-zÀ-ÿ\-\.\']+)*(?:\s*/\s*[A-Za-zÀ-ÿ\-\.\']+(?:\s+[A-Za-zÀ-ÿ\-\.\']+)*)?\s+[A-Z]+\s+\d+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.-]+)', text)
            
            current_rank = 1

            for block in skater_blocks[1:]:
                skater_match = skater_pattern.search(block)
                
                if skater_match:
                    rank = skater_match.group(1).strip()
                    skater_name_1 = skater_match.group(2).strip()
                    skater_name_2 = skater_match.group(3).strip() if skater_match.group(3) else None
                    noc = skater_match.group(4).strip()
                    starting_number = skater_match.group(5).strip()
                    total_segment_score = skater_match.group(6).strip()
                    total_element_score = skater_match.group(7).strip()
                    total_program_component_score = skater_match.group(8).strip()
                    total_deductions = skater_match.group(9).strip()

                    skater_id = f"{current_rank}_{skater_name_1}_{skater_name_2 if skater_name_2 else 'Single'}_{noc}_{segment}_{category}"

                    if "UNO Shoma" in skater_name_1 or (skater_name_2 and "UNO Shoma" in skater_name_2):
                        logging.info(f"Найден фигурист: {skater_name_1} / {skater_name_2 if skater_name_2 else ''}, NOC: {noc}, Ранг: {rank}, Программа: {segment}, Категория: {category}, {total_segment_score}, {total_element_score}, {total_program_component_score}, {total_deductions}")

                    executed_elements[skater_id] = []
                    program_components[skater_id] = []

                    if skater_id not in skaters_data:
                        skaters_data[skater_id] = {
                            'skater_id': skater_id,
                            'rank': current_rank,
                            'skater_name_1': skater_name_1,
                            'skater_name_2': skater_name_2 if skater_name_2 else None,
                            'noc': noc,
                            'starting_number': starting_number,
                            'segment': segment,
                            'category': category,
                            'total_segment_score': total_segment_score,
                            'total_element_score': total_element_score,
                            'total_program_component_score': total_program_component_score,
                            'total_deductions': total_deductions,
                        }

                        current_rank += 1

                    elements_section = re.search(r'Executed Elements(.+?)Program Components', block, re.DOTALL)
                    if elements_section:
                        elements_text = elements_section.group(1).strip()
                        element_matches = element_pattern.finditer(elements_text)
                        for match in element_matches:
                            element_number = match.group(1).strip()
                            element_name = match.group(2).strip()
                            info_symbol = match.group(3).strip() if match.group(3) else ''
                            base_value = match.group(4).strip()
                            x_symbol = match.group(5).strip() if match.group(5) else ''
                            goe = match.group(6).strip()
                            judge_scores = [match.group(i).strip() for i in range(7, 16)]
                            total_score = match.group(16).strip()

                            executed_elements[skater_id].append({
                                'element_number': element_number,
                                'element_name': element_name,
                                'info_symbol': info_symbol,
                                'base_value': base_value,
                                'x_symbol': x_symbol,
                                'goe': goe,
                                'judge_1': judge_scores[0],
                                'judge_2': judge_scores[1],
                                'judge_3': judge_scores[2],
                                'judge_4': judge_scores[3],
                                'judge_5': judge_scores[4],
                                'judge_6': judge_scores[5],
                                'judge_7': judge_scores[6],
                                'judge_8': judge_scores[7],
                                'judge_9': judge_scores[8],
                                'total_score': total_score,
                                'component_type': 'Element',
                            })

                    components_section = re.search(r'Program Components(.+?)Judges Total Program Component Score', block, re.DOTALL)
                    if components_section:
                        components_text = components_section.group(1).strip()
                        component_matches = component_pattern.finditer(components_text)
                        for match in component_matches:
                            component_name = match.group(1).strip()
                            factor = match.group(2).strip()
                            judge_scores = [match.group(i).strip() for i in range(3, 12)]
                            total_score = match.group(12).strip()

                            if "Factor" in component_name:
                                component_name = component_name.replace("Factor", "").strip()

                            program_components[skater_id].append({
                                'component_type': 'Program Component',
                                'element_name': component_name,
                                'judge_1': judge_scores[0],
                                'judge_2': judge_scores[1],
                                'judge_3': judge_scores[2],
                                'judge_4': judge_scores[3],
                                'judge_5': judge_scores[4],
                                'judge_6': judge_scores[5],
                                'judge_7': judge_scores[6],
                                'judge_8': judge_scores[7],
                                'judge_9': judge_scores[8],
                                'total_score': total_score,
                                'factor': factor,
                            })
    except Exception as e:
        logging.error(f"Ошибка при обработке файла {pdf_file}: {e}")

skaters_list = list(skaters_data.values())
executed_elements_list = []
for skater_id, elements in executed_elements.items():
    for element in elements:
        element['skater_id'] = skater_id
        executed_elements_list.append(element)

program_components_list = []
for skater_id, components in program_components.items():
    for component in components:
        component['skater_id'] = skater_id
        program_components_list.append(component)

if skaters_list:
    skaters_df = pd.DataFrame(skaters_list)
    skaters_df.to_excel('skaters.xlsx', index=False)
    logging.info("Данные о фигуристах сохранены в skaters.xlsx")

if executed_elements_list:
    executed_elements_df = pd.DataFrame(executed_elements_list)
    executed_elements_df.to_excel('executed_elements.xlsx', index=False)
    logging.info("Данные о выполненном элементе сохранены в executed_elements.xlsx")

if program_components_list:
    program_components_df = pd.DataFrame(program_components_list)
    program_components_df.to_excel('program_components.xlsx', index=False)
    logging.info("Данные о компонентах программы сохранены в program_components.xlsx")
