import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import time
import re
import pandas as pd
import os

source_dir = "E:/phi_3/new/"
destn_dir = "E:/phi_3/out_put/"

torch.random.manual_seed(0)

model = AutoModelForCausalLM.from_pretrained(
    "E:/phi_3/Phi-3-mini-4k-instruct", 
    # device_map="cuda", 
    torch_dtype="auto", 
    trust_remote_code=True, 
)
tokenizer = AutoTokenizer.from_pretrained("E:/phi_3/Phi-3-mini-4k-instruct")

# messages = [
#     # {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
#     # {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
#     {"role": "user", "content": "Suggest 20 utterances like 'I want to know my order status'"}
# ]

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

generation_args = {
    "max_new_tokens": 800,
    "return_full_text": False,
    # "temperature": 0.0,
    "do_sample": False,
}


def generate_response(text):
    messages = [{"role":"user","content":text}]
    start_time = time.time()
    output = pipe(messages, **generation_args)
    end_time = time.time()
    time_consumed = (end_time - start_time)//60
    utters = output[0]['generated_text']
    lines = [i.strip() for i in utters.strip().split('\n') if i.strip()]
    sentences = [i.split('. ',1)[1].strip() for i in lines]
    sentences_new = [re.sub(r'[^\w\s]', '', i) for i in sentences]
    print("Bot: ",sentences_new)
    print("time_consumed: ",time_consumed," minutes")
    return sentences_new




def get_batch_suit(source_dir,destn_dir):
    list_dir = os.listdir(source_dir)
    for i in list_dir:
        df = pd.read_csv(os.path.join(source_dir, i))
        utterances = list(df['input'])
        intent_name = list(df['intent'])[0]
        new_utterances = []
        for num, j in enumerate(utterances):
            print(num,"/",len(utterances))
            print(j)
            new = generate_response("suggest 10 utterances like '" + j + "' and must not deviate from the main context.")
            new_utterances.extend(new)
        utterances.extend(new_utterances)
        df_new = pd.DataFrame()
        df_new['input'] = pd.Series(utterances)
        df_new['intent'] = df_new['input'].apply(lambda x: intent_name if pd.notnull(x) else None)
        df_new.to_csv(os.path.join(destn_dir, i + '_new.csv'), index=False)
        print(df_new.head())
    return "Done"
    

get_batch_suit(source_dir,destn_dir)



