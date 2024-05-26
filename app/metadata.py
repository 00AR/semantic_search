import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import spacy
# Load the GPT-2 model and tokenizer from Hugging Face
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
gpt2_model = GPT2LMHeadModel.from_pretrained('distilgpt2')


# Load English model
nlp = spacy.load('en_core_web_sm')

def extract_metadata(text: str) -> tuple:
    doc = nlp(text)
    industry = []
    use_case = []
    geography = []
    for ent in doc.ents:
        if ent.label_ == "ORG" :
            industry.append(ent.text)
        elif ent.label_ == "GPE":
            geography.append(ent.text)
        elif ent.label_ == "PRODUCT":
            use_case.append(ent.text)

    return list(set(industry)), list(set(use_case)), list(set(geography))

# def refine_query(query: str) -> str:
#     # prompt = f"Refine the following search query to be more specific and relevant: {query}"
#     inputs = tokenizer.encode(query, return_tensors='pt')
#     outputs = gpt2_model.generate(inputs, max_length=50, num_return_sequences=1)
#     refined_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return refined_query


# case_studies = []
# with open('/home/dev/ar/repos/semantic_search/static/case_studies/case_studies.txt', 'r') as f:
#     case_studies = f.read().split("CASE_STUDY /\n")
# metadata = []
# for cs in case_studies:
#     metadata.append(extract_metadata(cs))

# for i in range(5):
#     print(metadata[i])