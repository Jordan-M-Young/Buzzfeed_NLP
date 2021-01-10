# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 10:50:37 2020

@author: jmyou
"""
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model = GPT2LMHeadModel.from_pretrained('./gpt2-titles')

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
input_ids = tokenizer.encode("10",
                             return_tensors='pt')

# set seed to reproduce results. Feel free to change the seed though to get different results
torch.manual_seed(10)
# activate sampling and deactivate top_k by setting top_k sampling to 0
sample_output = model.generate(
    input_ids, 
    do_sample=True, 
    max_length=1000, 
    top_k=0,
    temperature=0.7
)

print("Output:\n"  + 100 * '-')
print(tokenizer.decode(sample_output[0], skip_special_tokens=False))