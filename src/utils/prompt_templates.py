from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

fin_news_sentiment_template = """
    As a talented financial advisor, I need your help in analyzing the sentiment of the news. 
    What is the sentiment of this news? Please choose an answer from negative/neutral/positive
    {input} 
"""

fin_news_sentiment_multi_template = """
As a talented financial advisor, I need your help in analyzing the sentiment of the news. 
Analyze the sentiment of following news one by one. Please choose an answer from negative/neutral/positive. 

News: 
{input}

sentiment:
"""

fin_news_sentiment_examples = [
    {
        "input": "The interchange of Editors-in-Chief is a part of publisher 's goal to enhance job circulation in all personnel groups ",
        "output": "neutral"
    }, {
        "input": "$NQ got hit hard lower this AM --> looks like it has found support a 18.89 http:\/\/stks.co\/s052z",
        "output": "negative"
    }, {
        "input": "$IACI http:\/\/stks.co\/tJU Looks good on the weekly chart ",
        "output": "positive"
    }, {
        "input": "Amazon is set to raise the price of its Prime membership for the second time since 2014. A monthly subscription will soon cost $14.99.",
        "output": "negative"
    }, {
        "input": "$ESI on lows, down $1.50 to $2.50 BK a real possibility",
        "output": "negative"
    }, {
        "input": "Are ARM Holdings plc, Domino's Pizza Group plc and ASOS plc 3 must-have growth stocks?",
        "output": "neutral"
    }, {
        "input": "Sales of iPhone 14 are off to a sluggish start in China.",
        "output": "moderately negative"
    }, {
        "input": "Amazon's grocery deal with Morrisons is only the beginning",
        "output": "positive"
    }, {
        "input": "$HCP Come to the party and buy this -gonna give solid gains and a dividend $$$$$$",
        "output": "positive"
    }, {
        "input": "I see a 20 percent upside in $FB shares from here",
        "output": "positive"
    }, {
        "input": "The graphics specialist remains a solid bet despite near-term headwinds.",
        "output": "moderately positive"
    }
]

fin_news_sentiment_fs_template = """
    input: {input}
    output : {output}
"""


def one_shot_template(template):
    prompt = PromptTemplate(
        template=template,
        input_variables=['input']
    )
    return prompt


def few_shot_template_length_based(no_examples=None):
    prompt = PromptTemplate(template=fin_news_sentiment_fs_template,
                            input_variables=['input', 'output'])

    example_selector = LengthBasedExampleSelector(max_length=no_examples,
                                                  example_prompt=prompt,
                                                  examples=fin_news_sentiment_examples)

    fewshotprompt = FewShotPromptTemplate(example_selector=example_selector,
                                          example_prompt=prompt,
                                          input_variables=['input'],
                                          example_separator="\n",
                                          prefix="As a talented financial advisor, I need your help in analyzing the sentiment of the news. \n\n",
                                          suffix="\n\nWhat is the sentiment of this news? Please choose an answer from negative/neutral/positive:\n\ninput: {input}\noutput:",
                                          )
    return fewshotprompt


def few_shot_template(template):
    prompt = PromptTemplate(template=template,
                            input_variables=['input', 'output'])

    fewshotprompt = FewShotPromptTemplate(example_prompt=prompt,
                                          examples=fin_news_sentiment_examples,
                                          input_variables=['input'],
                                          example_separator="\n",
                                          prefix="As a talented financial advisor, I need your help in analyzing the sentiment of the news. \n\n",
                                          suffix="\n\nWhat is the sentiment of this news? Please choose an answer from negative/neutral/positive:\n\ninput: {input}\noutput:",
                                          )
    return fewshotprompt


def multi_template():
    multi_prompt = PromptTemplate(
        template=fin_news_sentiment_multi_template,
        input_variables=['inputs'])

    return multi_prompt


def summarization_prompt_template():
    summarization_template = """
        summarize the following text
        {text}
    """

    summarization_prompt = PromptTemplate(
        template=summarization_template,
        input_variables=['text']
    )

    return summarization_prompt


def translation_prompt_template():
    translation_template = """
    Translate the following text from {source_language} to {target_language} 
    {text}
    """

    translation_prompt = PromptTemplate(
        template=translation_template,
        input_variables=['text']
    )

    return translation_prompt
