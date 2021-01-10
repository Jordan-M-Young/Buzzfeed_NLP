# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 10:14:23 2020

@author: jmyou
"""

import json
from sklearn.model_selection import train_test_split
import re
from transformers import AutoTokenizer
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments,AutoModelWithLMHead
from transformers import pipeline
import torch
import csv
from transformers import GPT2LMHeadModel, GPT2Tokenizer




def build_text_files(data_json,dest_dir):
    f = open(dest_dir,'w',encoding='Utf-8')
    data = ''
    count = 0
    for texts in data_json:
        print(count)
        count += 1
        summary = str(texts).strip()
        summary = re.sub(r"\s", " ", summary)
        data += summary + "  "
    
    f.write(data)

    return data

def load_dataset(train_path,test_path,tokenizer):
    train_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=train_path,
          block_size=256)
     
    test_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=test_path,
          block_size=256)   
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset,test_dataset,data_collator

path = 'E:/PythonProjects/Buzzfeed_NLP/Text_Data.csv'
torch.cuda.is_available()
torch.cuda.device_count()

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

train_path = 'art_train_dataset.txt'
test_path = 'art_test_dataset.txt'

train_dataset,test_dataset,data_collator = load_dataset(train_path,test_path,tokenizer)
model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)


training_args = TrainingArguments(
    output_dir="./buzz-article-gpt-2", #The output directory
    overwrite_output_dir=True, #overwrite the content of the output directory
    num_train_epochs=3, # number of training epochs
    per_device_train_batch_size=4, # batch size for training
    per_device_eval_batch_size=4,  # batch size for evaluation
    eval_steps = 400, # Number of update steps between two evaluations.
    save_steps=800, # after # steps model is saved 
    warmup_steps=500,# number of warmup steps for learning rate scheduler
    )


trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset

)

trainer.train()
trainer.save_model()
tokenizer.save_pretrained(/buzz-article-gpt-2)
pip = pipeline('text-generation',model='./buzz-article-gpt-2', tokenizer='gpt2',config={'max_length':2000})
