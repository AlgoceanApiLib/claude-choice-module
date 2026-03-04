# 보조 로직 (프롬프트 정규화, 환경변수/모델 관리)
import os
from dotenv import load_dotenv

# 사용 가능한 모델 매핑
AVAILABLE_MODELS = {
    # ── Opus ──
    "opus-4.6": "claude-opus-4-6",            # Opus 4.6 (2026-02-05)
    "opus-4.5": "claude-opus-4-5-20251101",   # Opus 4.5 (2025-11-24)

    # ── Sonnet ──
    "sonnet-4.6": "claude-sonnet-4-6",          # Sonnet 4.6 (2026-02-17)
    "sonnet-4.5": "claude-sonnet-4-5-20250929", # Sonnet 4.5 (2025-09-29)

    # ── Haiku ──
    "haiku-4.5": "claude-haiku-4-5-20251001",  # Haiku 4.5 (2025-10-01)
}

# 환경변수에서 API 키 get 
def get_api_key():
    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print("⚠️ 경고: .env 파일이나 환경변수에 'ANTHROPIC_API_KEY'가 설정되지 않았습니다.")
    return key

# 입력된 프롬프트를 Claude 규격([{'role': 'user', 'content': ...}])으로 자동 변환
def normalize_prompt(prompt_input):
    if isinstance(prompt_input, str):
        return [{"role": "user", "content": prompt_input}]
    elif isinstance(prompt_input, dict):
        return [prompt_input]
    elif isinstance(prompt_input, list):
        return prompt_input
    else:
        raise ValueError(f"❌ 지원하지 않는 프롬프트 형식: {type(prompt_input)}")

# 프롬프트를 단일 문자열로 변환 (SUB 모드용 — Claude CLI는 문자열만 받음)
def prompt_to_string(prompt_input):
    if isinstance(prompt_input, str):
        return prompt_input
    elif isinstance(prompt_input, dict):
        return prompt_input.get("content", str(prompt_input))
    elif isinstance(prompt_input, list):
        # 대화 기록에서 마지막 user 메시지 추출
        for msg in reversed(prompt_input):
            if msg.get("role") == "user":
                return msg["content"]
        return prompt_input[-1].get("content", str(prompt_input[-1]))
    else:
        raise ValueError(f"❌ 지원하지 않는 프롬프트 형식: {type(prompt_input)}")