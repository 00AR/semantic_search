import textwrap
from uuid import uuid4
import PyPDF2
from bs4 import BeautifulSoup
from config import settings
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def read_pdf(file):
    """
    Read and the text from pdf
    """
    reader = PyPDF2.PdfReader(file)
    pdf_text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        pdf_text += page.extract_text() + "\n"
    return pdf_text


def text_to_pdf(text, output_filename):
    """
    Create a PDF file with the given text.
    """
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    max_width = width - 200
    avg_char_width = 7  # Adjust this value as needed based on font size
    max_chars_per_line = max_width // avg_char_width
    wrapped_lines = []
    for line in text.split('\n'):
        wrapped_lines.extend(textwrap.wrap(line, width=max_chars_per_line))  # Adjust width as needed
    
    y_position = height - 100  # Start from the top of the page
    
    for line in wrapped_lines:
        c.drawString(100, y_position, line)
        y_position -= 15
    c.save()


def clean_html(html_content: str):
    """
    Extract all the text from html
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    main_content = soup.find_all(['h1', 'h2', 'h3', 'p'])
    text = '\n'.join([tag.get_text(separator=" ", strip=True) for tag in main_content])
    return text

        
def clean_txt(txt_content: str):
    content = txt_content.split('\n')
    cleaned_content = []
    for line in content:
        if line:
            cleaned_content.append(line.strip())
    return cleaned_content


async def make_case_study_pdfs():
    case_studies = []
    with open(os.path.join(settings.BASE_DIR, 'samples','case_studies.txt'), 'r') as f:
        case_studies = f.read().split("CASE_STUDY /\n")
    # save these as new pdf files
    for i in range(1,34):
        uid = str(uuid4())
        filename = str(i) + '.pdf'
        filename = filename.replace(" ", "_")
        filename = f"{uid}_{filename}"
        filepath = os.path.join(settings.BASE_DIR ,settings.MEDIA, filename)
        content = case_studies[i]
        text_to_pdf(content, filepath)


def generate_case_studies():
    '''
    Extract case studies from the given samples and store them in a text file
    NOTE: Must be run only once
    '''
    for filename in os.listdir(os.path.join(settings.BASE_DIR, 'samples')):
        if filename.endswith('.txt'):
            with open(
                os.path.join(settings.BASE_DIR, 'samples', filename), 
                'r', 
                encoding='utf-8'
                ) as file:
                content = file.read()
                cleaned_text = clean_txt(content)
                # Finding starting and ending positions of Case Study in the sample document.
                start_idx = cleaned_text.index('customer stories /')
                end_idx = cleaned_text.index(
                    'We’re proud to be recognized as an industry leader, view our full list of honors to learn more.'
                    )
                case_study = cleaned_text[start_idx:end_idx]
                with open(os.path.join(settings.BASE_DIR, 'samples', 'case_studies.txt') , 'a') as f:
                    for line in case_study:
                        f.write(line)
                        f.write('\n')
    # NOTE: A little cleaning is done manually after this :D
    # But that can also be automated. A low priority task for now!

# RUN ONLY ONCE
# generate_case_studies()
# make_case_study_pdfs()

