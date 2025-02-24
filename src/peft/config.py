from peft import LoraConfig
from transformers import TrainingArguments
import torch

import logging

LOG = logging.getLogger(__name__)

class LoadTrainConfig():

    def __init__(self, model, model_id):
        self.model = model
        self.model_id = model_id
        self.loraConfig = self.loraConfig()
        self.trainargs = self.trainargs()

    def find_all_linear_names(self):
        cls = torch.nn.Linear
        lora_module_names = set()
        for name, module in self.model.named_modules():
            if isinstance(module, cls):
                names = name.split(".")
                lora_module_names.add(names[0] if len(names) == 1 else names[-1])

        if "lm_head" in lora_module_names:  # needed for 16-bit
            lora_module_names.remove("lm_head")
        return list(lora_module_names)

    def loraConfig(self):
        LOG.info('Loading lora configs')
        target_modules = self.find_all_linear_names()

        return  LoraConfig(
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=target_modules,
        )

    def trainargs(self):
        LOG.info('Loading training arguments')
        bf16_flag = False
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if device == 'cuda':
            print("Running on GPU")
            major, _ = torch.cuda.get_device_capability()
            if major >= 8:
                bf16_flag = True
                print("=" * 80)
            print("Your GPU supports bfloat16: accelerating training with --bf16")
            print("=" * 80)

        repo_id = self.model_id + 'sft'
        return TrainingArguments(
            output_dir= repo_id,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=8,
            learning_rate=5e-5,
            num_train_epochs=3,
            # PyTorch 2.0 specifics
            bf16=bf16_flag,  # bfloat16 training
            torch_compile=True,  # optimizations
            optim="adamw_torch",  # improved optimizer
            # logging & evaluation strategies
            logging_dir=f"{repo_id}/logs",
            logging_strategy="steps",
            logging_steps=200,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            save_total_limit=2,
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            # push to hub parameters
            # report_to="tensorboard"
        )

