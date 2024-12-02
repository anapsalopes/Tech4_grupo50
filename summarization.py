from docx import Document
from transformers import pipeline
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Especificar o modelo explicitamente
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def read_docx(docx_path):
    document = Document(docx_path)
    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)
    return "".join(full_text)

def chunk_text(text, max_chars=1000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def summarize_text(text, max_length=130, min_length=30, do_sample=False):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample)
    return summary[0]['summary_text']

def save_summary_to_txt(summary_text, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(summary_text)

if __name__ == "__main__":
    docx_path = 'relatorio_videoLeandro.docx'
    txt_path = 'resumo.txt'

    try:
        full_text = read_docx(docx_path)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {docx_path}")
        exit()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        exit()

    chunks = chunk_text(full_text)

    try:
        summaries = [summarize_text(chunk, max_length=200, min_length=50) for chunk in chunks]
        final_summary = " ".join(summaries)
        save_summary_to_txt(final_summary, txt_path)
        print("Sumarização completa. O resumo foi salvo em 'resumo.txt'.")
    except Exception as e:
        print(f"Erro durante a sumarização: {e}")
