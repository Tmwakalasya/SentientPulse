from transformers import BertTokenizer
import torch

print("Loading BERT tokenizer...")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
print("Tokenizer loaded")


def tokenize_data(text_data: str,tokenizer:BertTokenizer):
    encoded_inputs = tokenizer(
        text_data,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )
    return encoded_inputs

