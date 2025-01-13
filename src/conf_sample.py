import dataclasses
from pathlib import Path

THIS_DIR = Path(__file__).parent.resolve()

@dataclasses.dataclass
class Config:
    # カレンダーAPIのcredentailsのパス
    CREDENTIAL_APTH = THIS_DIR.joinpath("secret/gcal_credentials.json")

    # カレンダーAPIから最大何件取得するか
    API_MAX_RESULT = 400

    # APIトークンの保管場所
    TOKEN_PATH = THIS_DIR.joinpath("work/token.pickle")

    # OpenAI
    OPENAI_USE_AZURE_OPEN_AI = True
    OPENAI_API_KEY_PATH = THIS_DIR.joinpath("secret/openai.txt")
    OPENAI_MODEL_NAME = "gpt-4o"
    OPENAI_API_VERSION = "2024-02-01"
    OPENAI_AZURE_ENDPOINT = "https://xxx.openai.azure.com/"