import json

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer ,PreTrainedTokenizerFast,AutoConfig


from .sentiment_classifier import SentimentClassifier

with open("config.json") as json_file:
    config = json.load(json_file)


class Model:
    def __init__(self):

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(config["PRE_TRAINED_MODEL"])

        classifier = SentimentClassifier(len(config["CLASS_NAMES"]))
        classifier = classifier.eval()
        self.classifier = classifier.to(self.device)

    def predict(self, text):
        encoded_text = self.tokenizer(
            text,
            max_length=config["MAX_SEQUENCE_LEN"],
            truncation =True,
            return_tensors= "pt"
        )

        input_ids = encoded_text["input_ids"].to(self.device)
        attention_mask = encoded_text["attention_mask"].to(self.device)

        with torch.no_grad():
            probabilities = F.sigmoid(self.classifier(input_ids, attention_mask).logits).cpu().item()

        confidence, predicted_class = probabilities, int(probabilities > 0.5)
        return (
            config["CLASS_NAMES"][predicted_class],
            confidence,
        )


model = Model()


def get_model():
    return model
