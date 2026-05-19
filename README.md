# 🛡️ 생명보험 광고 심의 RAG 보조 시스템

보험 광고 문구를 입력하면 관련 법령 및 생명보험 광고 심의기준을 바탕으로  
**심의 리스크 · 문제 표현 · 위험 사유 · 수정 권장 문안**을 제시하는 Streamlit 앱입니다.

---

## 📂 폴더 구조

```
streamlit_app/
├── app.py                  # Streamlit 메인 앱
├── requirements.txt        # Python 의존성
├── packages.txt            # 시스템 패키지 (Streamlit Cloud용)
├── .streamlit/
│   └── config.toml         # Streamlit 테마 설정
├── data/                   # ⬅️ 여기에 법률 PDF 파일을 넣으세요
│   ├── 보험업법(...).pdf
│   ├── 개인정보 보호법(...).pdf
│   └── ...
└── db/                     # (자동 생성) ChromaDB 벡터 저장소
    └── chroma_db/
```

---

## 🚀 Streamlit Community Cloud 배포 방법

### 1단계: GitHub 리포지토리 만들기

1. GitHub에서 새 리포지토리를 생성합니다.
2. 이 폴더의 모든 파일을 push합니다.
3. **`data/` 폴더에 법률 PDF 8개를 함께 push합니다.**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2단계: Streamlit Cloud에서 앱 생성

1. [share.streamlit.io](https://share.streamlit.io) 에 접속 → GitHub 계정 연동
2. "New app" 클릭
3. 설정:
   - **Repository**: `YOUR_USERNAME/YOUR_REPO`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. "Deploy!" 클릭

### 3단계: 사용

- 배포 완료 후 앱 URL이 생성됩니다.
- 사이드바에서 **Gemini API Key**를 입력하고 사용하면 됩니다.
- API Key는 [Google AI Studio](https://aistudio.google.com/apikey)에서 무료 발급 가능합니다.

---

## 💻 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚠️ 참고사항

- **Streamlit Community Cloud 무료 플랜**: 리소스 제한이 있어 임베딩 모델 로딩에 시간이 걸릴 수 있습니다.
- **ChromaDB**: 첫 실행 시 PDF에서 벡터 DB를 빌드하며, 이후에는 `db/` 폴더에서 재사용합니다.
- **Gemini API 무료 티어**: 분당/일당 요청 제한이 있으니 429 에러 발생 시 잠시 후 재시도하세요.
- Streamlit Cloud에서 `db/` 폴더는 재배포 시 초기화될 수 있어, 매번 자동 빌드됩니다.
