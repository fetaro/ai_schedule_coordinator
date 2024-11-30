from pathlib import Path

THIS_DIR = Path(__file__).parent.resolve()

# カレンダーAPIのcredentailsのパス
CREDENTIAL_APTH = Path("/path/to/gcal_credentials.json")

# カレンダーAPIから最大何件取得するか
API_MAX_RESULT = 400

# APIトークンの保管場所
TOKEN_PATH = THIS_DIR.joinpath("work/token.pickle")

# OpenAI APIキーのパス
OPENAI_API_KEY_PATH = THIS_DIR.joinpath("secret/openai.txt")
