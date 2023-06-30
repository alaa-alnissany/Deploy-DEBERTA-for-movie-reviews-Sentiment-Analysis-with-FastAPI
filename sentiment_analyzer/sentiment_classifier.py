import json

from torch import nn
from transformers import AutoConfig, AutoModelForSequenceClassification

with open("config.json") as json_file:
    config = json.load(json_file)


class SentimentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.config = AutoConfig.from_pretrained(config["PRE_TRAINED_MODEL"])
        self.deberta = AutoModelForSequenceClassification.from_pretrained(config["PRE_TRAINED_MODEL"], config=self.config,)
        
    def forward(self, input_ids, attention_mask):
        output = self.deberta(input_ids=input_ids,attention_mask=attention_mask)
        return output
