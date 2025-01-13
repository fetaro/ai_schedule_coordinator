import logging
from typing import Optional

from openai import OpenAI, AzureOpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel

from conf import Config


class GptService:
    def __init__(
            self,
    ):
        self.gpt_model = Config.OPENAI_MODEL_NAME
        self.logger = logging.getLogger()
        api_key = open(Config.OPENAI_API_KEY_PATH, "r").read().strip()
        if Config.OPENAI_USE_AZURE_OPEN_AI:
            self.client = AzureOpenAI(api_key=api_key,
                                      api_version=Config.OPENAI_API_VERSION,
                                      azure_endpoint=Config.OPENAI_AZURE_ENDPOINT
                                      )
        else:
            self.client = OpenAI(api_key=api_key)
        self.gpt_parameters = {}

    def health_check(self):
        request_body = {
            "messages": [
                {
                    "role": "system",
                    "content": "OpenAIのAPIが正常に動作している場合は「OpenAIとの疎通に成功しました」と応答してください",
                },
                {"role": "user", "content": ""},
            ],
            "model": self.gpt_model,
        }
        request_body.update(self.gpt_parameters)
        chat_completion: ChatCompletion = self.client.chat.completions.create(
            **request_body
        )
        return chat_completion.choices[0].message.content

    def call_api(self, system_prompt: str, user_prompt: str, output_schema: Optional[type[BaseModel]] = None) -> str:
        request_body = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "model": self.gpt_model,
        }
        if output_schema is not None:
            # gpt-4o-2024-08-06 モデル以降であれば、response_formatを指定することで、出力のスキーマを指定できる
            # https://platform.openai.com/docs/guides/structured-outputs/chain-of-thought
            request_body["response_format"] = output_schema
        request_body.update(self.gpt_parameters)
        chat_completion: ChatCompletion = self.client.beta.chat.completions.parse(
            **request_body
        )
        # ChatCompletionの中身の例
        #
        # ChatCompletion(
        #                id='chatcmpl-xxxxx',
        #                choices=[
        #                         Choice(finish_reason='length',
        #                                index=0,
        #                                logprobs=None,
        #                                message=ChatCompletionMessage(content='',
        #                                                              role='assistant',
        #                                                              function_call=None,
        #                                                              tool_calls=None,
        #                                                              refusal=None))
        #                               ],
        #                created=1728017044,
        #                model='gpt-4-0613',
        #                object='chat.completion',
        #                service_tier=None,
        #                system_fingerprint=None,
        #                usage=CompletionUsage(
        #                                      completion_tokens=257,
        #                                      prompt_tokens=7936,
        #                                      total_tokens=8193,
        #                                      prompt_tokens_details={'cached_tokens': 0},
        #                                      completion_tokens_details={'reasoning_tokens': 0}
        #                                      )
        #                )

        # 最大文字数に達した場合はエラー
        if chat_completion.choices[0].finish_reason == "length":
            raise Exception(
                f"GPTの応答が最大文字数に達しました。completion_tokens={chat_completion.usage.completion_tokens}, "
                f"prompt_tokens={chat_completion.usage.prompt_tokens}, "
                f"total_tokens={chat_completion.usage.total_tokens}"
            )
        return chat_completion.choices[0].message.content
