import deeplake, os


def create_deeplake_dataset(dataset):
    return deeplake.dataset(f"hub://{os.getenv('ACTIVELOOP_ORG_ID')}/{dataset}")

def load_data_deeplake(dataset):
    pass

def formatting_prompts_func(sample):
    """Prepare the text from a sample of the dataset."""
    text = f"""
            {sample['instruction']}\n\n
            Content: {sample['input']}\n\n
            Sentiment: {sample['output']}
            """
    return text


def formatting_prompts_func_unpacked_dataset(examples):
    output_text = []
    for i in range(len(examples["instruction"])):
        instruction = examples["instruction"][i]
        input_text = examples["input"][i]
        response = examples["output"][i]

        if len(input_text) >= 2:
            context = f"""
            Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
            """
            text = f''' {context}            
            ### Instruction:
            {instruction}
            ### Input:
            {input_text}
            ### Response:
            {response}
            '''
        else:
            text = f''' {context}
             ### Instruction:
            {instruction}
            ### Response:
            {response}
            '''
        output_text.append(text)

    return output_text