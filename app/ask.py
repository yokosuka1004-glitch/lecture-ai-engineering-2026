
"""第1回: 会話履歴を保持してLLMに質問するスクリプト。"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str, history: list, client) -> str:
    # 今回の質問を履歴に追加
    history.append({
        "role": "user",
        "parts": [{"text": question}]
    })

    try:
        # 過去の会話を含めてAIに送信
        response = client.models.generate_content(
            model=MODEL,
            contents=history,
        )
    except Exception:
        # APIエラー時は未回答の質問を履歴から取り除く
        history.pop()
        raise

    # トークン数を表示
    usage = response.usage_metadata
    if usage is not None:
        print(f"[入力トークン数] {usage.prompt_token_count}")
        print(f"[出力トークン数] {usage.candidates_token_count}")
    else:
        print("[トークン数] 取得できませんでした")

    answer = response.text or ""

    # AIの回答も履歴に追加
    history.append({
        "role": "model",
        "parts": [{"text": answer}]
    })

    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description="LLMと連続して会話する")
    parser.add_argument("question", nargs="?", default=None)
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())
    history = []

    print(f"[model] {MODEL}")
    print("AIとの会話を開始します。")
    print("終了するには exit と入力してください。")

    question = args.question

    while True:
        if question is None:
            try:
                question = input("\nあなた: ")
            except (EOFError, KeyboardInterrupt):
                print("\n会話を終了します。")
                break

        if question.strip().lower() == "exit":
            break

        if not question.strip():
            question = None
            continue

        try:
            answer = ask(question, history, client)
            print(f"\nAI: {answer}")
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            print(f"[API code] {e.code}")
            print(f"[API message] {e.message}")
            raise SystemExit(1)

        question = None


if __name__ == "__main__":
    main()
