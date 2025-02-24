from datasets import load_dataset, DatasetDict, ClassLabel
from transformers import (AutoTokenizer,
                          AutoModelForSequenceClassification,
                          )
from trl import SFTTrainer
from dataprep import formatting_prompts_func_unpacked_dataset
from config import LoadTrainConfig
import torch
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s APPLOG:%(name)-12s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H: %M")

LOG = logging.getLogger(__name__)


class LLMTuner():
    def __init__(self, model_id, dataset_id, split_dataset_pct=None, training_args=None, trainer=None, bnb_config=None, peft_config=None):
        self.model_id = model_id
        self.dataset_id = dataset_id
        self.training_args=training_args
        self.bnb_config = bnb_config
        self.peft_config=peft_config
        self.trainer = trainer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.dataset = load_dataset(self.dataset_id, split='train')
        self.split_dataset_pct = split_dataset_pct

        if self.split_dataset_pct:
            label_names = sorted(set(self.dataset["output"]))
            dataset = self.dataset.cast_column("output", ClassLabel(names=label_names))
            train_test_dataset = dataset.train_test_split(test_size=0.3)
            test_valid_dataset = train_test_dataset['test'].train_test_split(test_size=0.5)

            self.dataset = DatasetDict({
                'train': train_test_dataset['train'],
                'test': test_valid_dataset['test'],
                'valid': test_valid_dataset['train']})

            print(self.dataset)


    def training_func(self):

        label_names = sorted(set(self.dataset["train"]["output"]))
        num_labels = len(label_names)
        label2id, id2label = dict(), dict()
        for i, label in enumerate(label_names):
            label2id[label] = str(i)
            id2label[str(i)] = label

        model = AutoModelForSequenceClassification.from_pretrained(self.model_id,
                                                                   num_labels=num_labels,
                                                                   label2id=label2id,
                                                                   id2label=id2label)
        train_config = LoadTrainConfig(model, self.model_id)

        trainer = SFTTrainer(
            model,
            tokenizer=self.tokenizer,
            peft_config=train_config.loraConfig,
            args=train_config.trainargs,
            train_dataset=self.dataset['train'],
            eval_dataset=self.dataset['valid'],
            formatting_func=formatting_prompts_func_unpacked_dataset,
            max_seq_length=256,
            packing=False
        )

        return trainer

    def tune(self):
        trainer = self.training_func()
        LOG.info(trainer.model.print_trainable_parameters())
        #return trainer
        trainer.train()


if __name__ == "__main__":
    # model_id = 'distilbert-base-uncased-finetuned-sst-2-english'
    LOG.info('job started')
    model_id = 'distilbert-base-uncased'
    tuner = LLMTuner(model_id=model_id,
                     dataset_id='FinGPT/fingpt-sentiment-train',
                     split_dataset_pct=0.3)

    tuner.tune()





