from .utils import get_api_key, AVAILABLE_MODELS, normalize_prompt, prompt_to_string

def help():
    print("\n=== choice_claude 사용 설명서 ===\n")
    print(" help()        — 이 설명서 출력")
    print(" help_call()   — 지원하는 호출 방식 (SDK / API / SUB) 안내")
    print(" help_Model()  — 지원하는 모델 별칭 목록 출력")
    print(" help_api()    — API 키 발급 방법 안내")
    print(" run()         — Claude 모델 호출")
    print("                  run(Call_rule, Model_name, prompt, max_tokens=1024)\n")
    print(" ── 과금 체계 ──")
    print(" SDK / API : API 크레딧 사용 (console.anthropic.com 종량제)")
    print(" SUB       : Claude 구독 크레딧 사용 (Pro/Max 구독)")
    print(" * 두 과금 체계는 완전히 별도입니다. 서로 영향 없음.\n")

def help_call():
    print("\n=== 지원하는 호출 방식 (Call_rule) ===")
    print(" 1. 'SDK' : Anthropic 공식 파이썬 라이브러리 사용 (API 키 필요)")
    print(" 2. 'API' : requests 라이브러리를 통한 REST 직접 호출 (API 키 필요)")
    print(" 3. 'SUB' : Claude 구독 크레딧으로 호출 (API 키 불필요, Claude Code CLI 필요)")
    print("            * SDK/API보다 느림 (CLI 초기화 5~15초)")
    print("            * Claude Code 시스템 프롬프트가 적용된 응답 (코딩 도우미 역할)\n")
    return ["SDK", "API", "SUB"]

def help_Model():
    print("\n=== 지원하는 모델 별칭 목록 ===")
    for alias, real_name in AVAILABLE_MODELS.items():
        print(f" - {alias}  →  {real_name}")
    print("* 위 목록에 없는 최신 모델명을 직접 입력해도 작동합니다.\n")
    return list(AVAILABLE_MODELS.keys())

def help_api():
    print("\n=== API 키 발급 방법 ===\n")
    print(" 1. https://console.anthropic.com 접속")
    print(" 2. 로그인 후 Settings → API Keys 이동")
    print(" 3. 'Create Key' 클릭 → 키 복사 (sk-ant-...)")
    print(" 4. 프로젝트 최상단에 .env 파일 생성:")
    print("    ANTHROPIC_API_KEY=sk-ant-여기에_복사한_키_붙여넣기\n")
    print(" * API 키는 종량제 과금입니다 (구독 크레딧과 별도)")
    print(" * 구독만 사용하려면 API 키 없이 Call_rule='SUB' 사용\n")

def run(Call_rule: str, Model_name: str, prompt, max_tokens: int = 1024):
    if not Model_name:
        Model_name = "sonnet-4.6"

    exact_model_name = AVAILABLE_MODELS.get(Model_name, Model_name)
    rule = Call_rule.upper()

    # [SDK 방식] - API 키 필요, Anthropic 공식 라이브러리 사용
    if rule == "SDK":
        api_key = get_api_key()
        if not api_key:
            raise ValueError("API 키가 없습니다. .env 파일에 'ANTHROPIC_API_KEY'를 설정하세요.")

        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("'anthropic' 패키지가 설치되지 않았습니다. SDK 방식을 쓰려면 설치해주세요.")

        messages = normalize_prompt(prompt)
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=exact_model_name,
            max_tokens=max_tokens,
            messages=messages
        )
        return response.content[0].text

    # [API 방식] - API 키 필요, requests를 통한 REST 직접 호출
    elif rule == "API":
        api_key = get_api_key()
        if not api_key:
            raise ValueError("API 키가 없습니다. .env 파일에 'ANTHROPIC_API_KEY'를 설정하세요.")

        try:
            import requests
        except ImportError:
            raise ImportError("'requests' 패키지가 설치되지 않았습니다. API 방식을 쓰려면 설치해주세요.")

        messages = normalize_prompt(prompt)
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": exact_model_name,
            "max_tokens": max_tokens,
            "messages": messages
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"API 에러 {response.status_code}: {response.text}")
        return response.json()['content'][0]['text']

    # [SUB 방식] - API 키 불필요, Claude 구독 크레딧 사용 (Claude Code CLI 필요)
    # 주의: Claude Code CLI 초기화로 인해 SDK/API 대비 응답이 느림 (5~15초)
    elif rule == "SUB":
        import subprocess
        import shutil
        import os

        if os.environ.get("CLAUDECODE"):
            raise RuntimeError(
                "Claude Code 세션 내부에서는 SUB 방식을 사용할 수 없습니다. "
                "독립 터미널에서 실행하거나, SDK/API 방식을 사용하세요."
            )

        if not shutil.which("claude"):
            raise RuntimeError(
                "Claude Code CLI가 설치되지 않았습니다. "
                "'npm install -g @anthropic-ai/claude-code'로 설치하고 로그인하세요."
            )

        prompt_str = prompt_to_string(prompt)
        cmd = [
            "claude", "-p", prompt_str,
            "--model", exact_model_name,
            "--output-format", "text"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI 에러: {result.stderr.strip()}")

        return result.stdout.strip()

    else:
        raise ValueError("잘못된 Call_rule입니다. 'SDK', 'API', 'SUB' 중 하나를 사용하세요.")