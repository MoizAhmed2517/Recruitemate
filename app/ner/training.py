import spacy
from spacy.training.example import Example
from spacy.tokens import DocBin
import json

# Load pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Add 'ner' pipeline if not present
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Load training data
with open("training_data/ner_training_data_readable.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Add PERSON entity to the pipeline
for item in data:
    for ent in item["entities"]:
        ner.add_label(ent["label"])

# Convert training data into spaCy's format
train_examples = []
for item in data:
    text = item["text"]
    annotations = {"entities": [(ent["start"], ent["end"], ent["label"]) for ent in item["entities"]]}
    train_examples.append(Example.from_dict(nlp.make_doc(text), annotations))

# Disable other pipelines to focus on 'ner'
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()
    
    # Train for multiple iterations
    for epoch in range(30):  # You can increase/decrease based on accuracy
        losses = {}
        nlp.update(train_examples, drop=0.3, losses=losses)
        print(f"Epoch {epoch + 1}, Loss: {losses['ner']}")

# Save the fine-tuned model
nlp.to_disk("pak_names_ner_model")

# Load and test the model
nlp_custom = spacy.load("pak_names_ner_model")
test_text = "2/13/2025 11:05:30 Wahab Ali 03456395334 wahabalibb7@gmail.com 2-3 years 1-2 year 2-3 years 1-2 year 1-2 year Yes https://drive.google.com/open?id=1NtBRjBwe20tZGVF12hxLRX-9IUuOJgau wahabalibb7@gmail.com"
doc = nlp_custom(test_text)

print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
