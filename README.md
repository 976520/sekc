# Sekc Programming Language

이 프로젝트는 **Sekc** 언어의 레퍼런스 구현체입니다.
7가지 언어를 혼용하여 각 언어의 장점을 살린 **Polyglot Pipeline** 구조로 설계되었습니다.

## 🏗 아키텍처 (Architecture)

컴파일 및 실행 과정은 다음 순서로 파이프라인을 타고 흐릅니다.

1. **Driver (Java)**: 전체 프로세스 실행 및 조정 관리
2. **Lexer (Rust)**: 소스 코드를 읽어 토큰(Token)으로 변환 (들여쓰기 처리 강점)
3. **Parser (Kotlin)**: 토큰을 받아 추상 구문 트리(AST) 생성 (강력한 타입 시스템)
4. **Analyzer (Python)**: AST를 검증하고 시맨틱 체크 (유연한 로직 검사)
5. **Runtime (C)**: 고성능 메모리/수학 연산 코어 라이브러리
6. **Interpreter (C++)**: AST를 순회하며 실제 프로그램 실행

## 🚀 실행 방법 (How to Run)

프로젝트 루트에서 다음 명령어를 실행하여 빌드 및 테스트를 수행할 수 있습니다.

```bash
chmod +x run.sh
./run.sh

./sekc test.sekc
```

### 필수 요구 사항 (Prerequisites)
각 언어의 컴파일러가 시스템에 설치되어 있어야 합니다:
- `cargo` (Rust)
- `kotlinc` (Kotlin)
- `python3` (Python)
- `gcc` / `g++` (C/C++)
- `javac` / `java` (Java)

만약 일부 도구가 없다면 `build_and_run.sh` 스크립트는 해당 단계를 모의(mock) 처리하거나 건너뜁니다.
