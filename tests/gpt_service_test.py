from gpt_service import GptService


def test_call_api():
    gpt_service = GptService()
    res = gpt_service.call_api(
        system_prompt="これはAPIのテストです。user_promptに入力した単語を2回繰り返して返答してください。それ以外の言葉を使ってはいけません。",
        user_prompt="Hello",
    )
    assert res == "Hello Hello"
