import pandas as pd
import random
import json
from itertools import cycle

pakistani_names = pd.read_csv('training_data/ner_dataset.csv', encoding="ISO-8859-1")
names_list = pakistani_names['Muslim Names'].dropna().tolist()  # Remove NaNs
sentence_templates = json.load(open('training_data/sentence_template.json', encoding='utf-8'))['sentence_template']

random.shuffle(names_list)
names_cycle = cycle(names_list)
TRAINING_EXAMPLES = 10000

# Generate training data
TRAIN_DATA = []
for _ in range(TRAINING_EXAMPLES): 
    template = random.choice(sentence_templates)
    num_names_needed = template.count("{}")
    names = [next(names_cycle) for _ in range(num_names_needed)]
    sentence = template.format(*names)

    entities = []
    start = 0
    for name in names:
        start = sentence.find(name, start)
        end = start + len(name)
        entities.append({
            "entity": name,
            "start": start,
            "end": end,
            "label": "PERSON"
        })
        start = end  # Move start forward to avoid duplicate matches

    TRAIN_DATA.append({
        "text": sentence,
        "entities": entities
    })

with open("training_data/ner_training_data_readable.json", "w", encoding="utf-8") as f:
    json.dump(TRAIN_DATA, f, indent=4, ensure_ascii=False)

print("Formatted JSON saved successfully!")
