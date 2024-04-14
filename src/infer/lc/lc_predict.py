from langchain_google_vertexai import VertexAIModelGarden
import vertexai
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_vertexai import VertexAI
from prompt_templates import *
from langchain_community.callbacks import get_openai_callback
import logging

LOG = logging.getLogger(__name__)


class LCPredict():
    def __init__(self, llm):
        self.llm = llm

    def _predict_with_template(self, template, input, **kwargs):
        llmchain = LLMChain(prompt=template, llm=self.llm)
        return llmchain.predict(text=input, **kwargs)

    def translate(self, text, source_language, target_language):
        return self._predict_with_template(translation_prompt_template(),
                                           text,
                                           source_language=source_language,
                                           target_language=target_language)

    def summarize(self, text):
        return self._predict_with_template(summarization_prompt_template(), text)

    # def summarize(self, text):
    #     llmchain = LLMChain(prompt=summarization_prompt_template(),
    #                         llm=self.llm)
    #     with get_openai_callback() as cb:
    #         result = llmchain.predict(text=text)
    #         LOG.info(f'cost for the call : {cb}')
    #
    #     return result

    def pred(self, input, template):
        llmchain = LLMChain(prompt=template,
                            llm=self.llm)

        res = llmchain.invoke(input)
        return res

    def pred_multi_str(self, input, template):
        llmchain = LLMChain(prompt=template,
                            llm=self.llm)

        res = llmchain.run(input)
        return res

    def few_shot_invoke_length_based(self, input, template):
        llmchain = LLMChain(prompt=few_shot_template(template),
                            llm=self.llm)

        res = llmchain.generate(input)
        return res


if __name__ == "__main__":
    llm = VertexAI(model_name="gemini-pro")
    lcpredict = LCPredict(llm)

    # res = lcpredict.summarize(
    #     "LangChain provides many modules that can be used to build language model applications. "
    #     "Modules can be combined to create more complex applications, or be used individually for simple applications. "
    #     "The most basic building block of LangChain is calling an LLM on some input. Let’s walk through a simple example of how to do this. "
    #     "For this purpose, let’s pretend we are building a service that generates a company name based on what the company makes.")
    #
    # print(res + '\n')

    res = lcpredict.translate('How are you?','English', 'Hindi')
    print(res + '\n')

    # input = {
    #     'input': "$YMI http:\/\/stks.co\/Xyf Long setup. Closed above the 20MA. MACD cross. November catalyst.",
    # }
    # res = lcpredict.pred(input, one_shot_template(fin_news_sentiment_template))
    # print(res)
    #
    # inputs = [
    #     {'input': "$YMI http:\/\/stks.co\/Xyf Long setup. Closed above the 20MA. MACD cross. November catalyst."},
    #     {'input': "Berkshire Hathaway names Kara Raiguel to lead General Re unit"},
    #     {'input': "NOBL starts the year on a sour note losing 4.08% in January."},
    # ]
    #
    # res = lcpredict.pred(inputs, few_shot_template(fin_news_sentiment_template))
    # print(res + '\n')
    # res = lcpredict.few_shot_invoke_length_based(inputs, few_shot_template_length_based(10))
    # print(res + '\n')
    #
    # input_str = (
    #         "$YMI http:\/\/stks.co\/Xyf Long setup. Closed above the 20MA. MACD cross. November catalyst.\n" +
    #         "NOBL starts the year on a sour note losing 4.08% in January.\n"
    # )
    #
    # res = lcpredict.pred(input_str, multi_template())

# PROJECT_ID = "471026294913"
# REGION = "us-west1"
# llm = VertexAIModelGarden(project=PROJECT_ID,
#                           location=REGION,
#                           endpoint_id="7052909695345885184"
#                           )

#
# # Initialize Vertex AI SDK
# vertexai.init(project=PROJECT_ID, location=REGION)
