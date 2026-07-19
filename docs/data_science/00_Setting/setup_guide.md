
# VS Code 프로젝트 전용 Conda 가상 환경 세팅 가이드 (Python 3.7)
- PC의 시스템 환경 변수(PATH)를 오염시키지 않고, VS Code로 특정 프로젝트 폴더를 열었을 때만 자동으로 Conda 가상 환경이 활성화되도록 구성하는 격리 세팅 방법

## 📌 사전 준비
- **Miniconda 설치** 
  - 단, 설치 중 `Advanced Options`에서 `Add Miniconda3 to my PATH environment variable` 옵션은 반드시 **체크 해제**하여 기존 시스템 환경을 보호한다.
- **VS Code 설치**

---

## 🚀 1단계: 프로젝트 폴더 내 가상 환경 생성

Conda 명령어를 인식하는 전용 터미널을 사용하여 프로젝트 폴더 내부에 환경을 설치한다.

1. 윈도우 시작 메뉴에서 **`Anaconda Prompt (Miniconda3)`**를 실행한다.
2. 작업할 프로젝트 폴더로 이동한다.
    ```bash
      cd [프로젝트 폴더 절대경로]
    ```

3. 현재 폴더 내에 가상환경인 (`.venv`) Python 3.7 환경을 생성한다.
    ```bash
    conda create -p ./.venv python=3.7
    ```

---

## ⚙️ 2단계: VS Code 자동 활성화 설정 (settings.json)

이 세팅의 핵심이다. 일반 터미널(CMD)이 이 폴더에서 열릴 때, 백그라운드에서 Conda 스크립트를 주입하여 환경을 강제로 켜도록 만든다.

1. VS Code에서 해당 프로젝트 폴더를 최상위 경로로 연다.
2. `Ctrl + Shift + P` ➔ `Preferences: Open Workspace Settings (JSON)`을 클릭한다.
3. 열린 `.vscode/settings.json` 파일에 아래 코드를 작성한다. (본인의 PC 환경에 맞게 `[경로]` 부분을 수정하여 사용한다.)
    ```json
    {
      "python.defaultInterpreterPath": "[프로젝트폴더 절대경로]\\.venv\\python.exe",
      "terminal.integrated.defaultProfile.windows": "Command Prompt",
      "terminal.integrated.profiles.windows": {
        "Command Prompt": {
          "path": "cmd.exe",
          "args": [
            "/K", 
            "C:\\Users\\[사용자이름]\\miniconda3\\Scripts\\activate.bat [프로젝트폴더 절대경로]\\.venv"
          ]
        }
      }
    }
    ```
4. 저장(`Ctrl + S`) 후 기존 터미널을 끄고 새 터미널(`Ctrl + ~`)을 연다.
5. 터미널 경로 맨 앞에 `(.venv)`가 나타나는지 확인한다.

---

## 📦 3단계: 필수 패키지 설치
- 터미널 프롬프트 앞에 `(.venv)`가 활성화된 상태에서 실습에 필요한 패키지들을 설치한다.
    ```bash
    # Pandas 설치
    conda install -c conda-forge pandas -y

    # Scikit-Learn 설치 (패키지명 주의: sklearn이 아님)
    conda install -c conda-forge scikit-learn -y
    ```

---

## 🛡️ 4단계: Git 추적 제외 설정 (.gitignore)
- 가상 환경 폴더와 대용량 데이터가 Github에 통째로 올라가지 않도록 제외 처리한다.
1. 프로젝트 최상위 경로에 `.gitignore` 파일을 생성한다.
2. 아래 내용을 추가하고 저장한다.
    ```text
    # Conda 가상 환경 폴더 제외
    .venv/

    # Python 캐시 파일 제외
    __pycache__/
    ```


3. 터미널에서 `.gitignore` 파일만 먼저 푸시하여 안전하게 무시 설정을 반영한다.
    ```cmd
    git add .gitignore
    git commit -m "Add .gitignore to exclude virtual environment"
    git push
    ```