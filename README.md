## choice_claude

`choice_claude`는 Anthropic의 Claude AI 모델을 호출할 때, **SDK / REST API / 구독 크레딧** 세 가지 방식을 단 한 줄의 코드로 자유롭게 스위칭할 수 있도록 도와주는 파이썬 래퍼(Wrapper) 패키지입니다.

다양한 형태의 프롬프트(문자열, 딕셔너리, 대화 기록 리스트)를 자동으로 전처리하여, 복잡한 데이터 가공 없이 즉시 AI 에이전트나 웹 서비스 백엔드에 연동할 수 있습니다.

## 주요 기능

* **3가지 호출 방식**: `SDK` (공식 라이브러리), `API` (REST 직접 호출), `SUB` (구독 크레딧)
* **자동 프롬프트 정규화**: `str`, `dict`, `list` 등 어떤 형태로 프롬프트를 넘겨도 자동 변환
* **모델 별칭(Alias) 지원**: `sonnet-4.6`, `opus-4.6` 등 직관적인 이름으로 호출
* **의존성 자동 관리**: 패키지 설치 시 필수 라이브러리 자동 설치

---

## 호출 방식 비교

| Call_rule | 인증 방식 | 필요 패키지 | 대상 |
|---|---|---|---|
| `"SDK"` | API 키 (.env) | `anthropic` | API 키 보유자 |
| `"API"` | API 키 (.env) | `requests` | API 키 보유자 |
| `"SUB"` | 구독 크레딧 (자동) | Claude Code CLI | Claude 구독자 (API 키 불필요) |

---

## 설치 방법

### 1. GitHub에서 직접 설치

```bash
pip install git+https://github.com/AlgoceanApiLib/claude-choice-module.git
```

### 2. 저장소 클론 후 설치

```bash
git clone https://github.com/AlgoceanApiLib/claude-choice-module.git
cd claude-choice-module
pip install -e .
```

### 3. 폴더 복사 후 직접 사용 (Drop-in)

`choice_claude/` 폴더를 프로젝트에 복사하고 직접 import:

```python
from choice_claude import run
```

> **참고**: drop-in 방식에서는 필요한 패키지를 별도로 설치해야 합니다.

---

## 환경 설정

### SDK / API 방식 (API 키 필요)

프로젝트 최상단 디렉토리에 `.env` 파일을 생성:

```env
ANTHROPIC_API_KEY=본인의_실제_클로드_키
```

API 키는 [console.anthropic.com](https://console.anthropic.com/settings/keys)에서 발급받을 수 있습니다.

### SUB 방식 (구독 크레딧)

API 키가 필요 없습니다. 대신 아래 조건이 필요합니다:

1. **Claude Code CLI 설치**: `npm install -g @anthropic-ai/claude-code`
2. **Claude Code 인증 완료**: `claude` 명령어로 로그인된 상태
3. **Claude Max 플랜 사용 권장** (멀티턴 대화 시 요약 호출이 추가되어 토큰 소모 증가)

---

## 사용 방법

### 1. 사용 가능한 옵션 확인

```python
import choice_claude

# 지원하는 호출 방식(SDK/API/SUB) 출력
choice_claude.help_call()

# 지원하는 모델 목록과 별칭 출력
choice_claude.help_Model()
```

### 2. SDK 방식 (API 키 사용)

```python
import choice_claude

response = choice_claude.run(
    Call_rule="SDK",
    Model_name="sonnet-4.6",
    prompt="리액트 함수형 컴포넌트의 장점을 한 줄로 설명해줘."
)
print(response)
```

### 3. API 방식 (API 키 사용)

```python
import choice_claude

chat_history = [
    {"role": "user", "content": "안녕, 넌 누구니?"},
    {"role": "assistant", "content": "저는 클로드입니다."},
    {"role": "user", "content": "너를 만든 곳은?"}
]

response = choice_claude.run("API", "haiku-4.5", chat_history)
print(response)
```

### 4. SUB 방식 (구독 크레딧, API 키 불필요)

```python
import choice_claude

response = choice_claude.run(
    Call_rule="SUB",
    Model_name="sonnet-4.6",
    prompt="안녕을 영어로 한 단어로 말해."
)
print(response)
```

### 5. SUB 방식 멀티턴 대화

```python
import choice_claude

chat_history = [
    {"role": "user", "content": "안녕, 넌 누구니?"},
    {"role": "assistant", "content": "저는 클로드입니다."},
    {"role": "user", "content": "너를 만든 곳은?"}
]

response = choice_claude.run("SUB", "sonnet-4.6", chat_history)
print(response)
```

> SUB 멀티턴은 대화 기록을 문자열로 변환하여 전달합니다.
> 대화가 길어지면(컨텍스트 50% 초과) 이전 대화를 AI가 자동 요약하여 토큰을 절약합니다.
> 요약 시 sonnet-4.6으로 추가 호출이 발생하므로 **Max 플랜 권장**입니다.

---

## 지원 모델 별칭

| 별칭 | 실제 모델명 |
|---|---|
| `opus-4.6` | `claude-opus-4-6` |
| `opus-4.5` | `claude-opus-4-5-20251101` |
| `sonnet-4.6` | `claude-sonnet-4-6` |
| `sonnet-4.5` | `claude-sonnet-4-5-20250929` |
| `haiku-4.5` | `claude-haiku-4-5-20251001` |

> 위 목록에 없는 최신 모델명을 직접 입력해도 작동합니다.

---

## 프로젝트 구조

```text
choice_claude/
├── pyproject.toml         # 패키지 설정 및 의존성 정의
├── README.md              # 프로젝트 설명서
├── LICENSE                # Apache License 2.0
├── .env.example           # 환경 변수 템플릿
├── .gitignore             # Git 제외 파일 목록
└── choice_claude/         # 핵심 모듈 패키지
    ├── __init__.py        # 외부 인터페이스 (run, help_call, help_Model 노출)
    ├── core.py            # 메인 실행 로직 (SDK/API/SUB 호출)
    └── utils.py           # 프롬프트 전처리 및 환경변수/모델 관리
```

---

## License

Apache License 2.0 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
