import streamlit as st
import os
import re
from pathlib import Path

# ──────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="생명보험 광고 심의 RAG 시스템",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# 커스텀 CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
  }
  .block-container {
    max-width: 960px;
    padding-top: 2rem;
    padding-bottom: 2rem;
  }

  /* 헤더 */
  .app-header {
    background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
    border-radius: 16px;
    padding: 2.4rem 2.8rem;
    margin-bottom: 2rem;
    color: #fff;
  }
  .app-header h1 {
    font-size: 1.65rem;
    font-weight: 700;
    margin: 0 0 .45rem 0;
    letter-spacing: -0.02em;
  }
  .app-header p {
    font-size: 0.88rem;
    color: rgba(255,255,255,.72);
    margin: 0;
    line-height: 1.65;
  }
  .app-header .badge {
    display: inline-block;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 500;
    color: rgba(255,255,255,.85);
    margin-bottom: .8rem;
    letter-spacing: 0.04em;
  }

  /* 법률 태그 */
  .law-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 1rem;
  }
  .law-tag {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.72rem;
    color: rgba(255,255,255,.7);
  }

  /* 키워드 경고 */
  .keyword-alert {
    background: #FFF7ED;
    border-left: 4px solid #F59E0B;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.4rem;
    margin-bottom: 1.2rem;
  }
  .keyword-alert .title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #92400E;
    margin-bottom: .3rem;
  }
  .keyword-alert .kw {
    display: inline-block;
    background: #FEF3C7;
    border-radius: 4px;
    padding: 1px 8px;
    margin: 2px 4px 2px 0;
    font-size: 0.82rem;
    font-weight: 500;
    color: #B45309;
  }

  /* 결과 카드 */
  .result-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.6rem 2rem;
    margin-bottom: .8rem;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
  }
  .result-card .section-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #1E293B;
    margin: 0 0 .6rem 0;
    padding-bottom: .4rem;
    border-bottom: 2px solid #E2E8F0;
  }
  .result-card .content {
    font-size: 0.84rem;
    color: #475569;
    line-height: 1.8;
    white-space: pre-wrap;
  }

  /* 위험도 뱃지 */
  .risk-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    margin: .4rem 0;
  }
  .risk-low    { background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }
  .risk-mid    { background: #FFF7ED; color: #92400E; border: 1px solid #FED7AA; }
  .risk-high   { background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }
  .risk-severe { background: #FEF2F2; color: #7F1D1D; border: 1px solid #FCA5A5; }

  /* 면책 푸터 */
  .disclaimer {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    font-size: 0.76rem;
    color: #94A3B8;
    line-height: 1.6;
    margin-top: 2rem;
  }

  /* API Key 섹션 */
  .api-section {
    background: #F1F5F9;
    border: 1px dashed #CBD5E1;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
  }
  .api-section .label {
    font-size: 0.76rem;
    font-weight: 600;
    color: #64748B;
    letter-spacing: 0.04em;
    margin-bottom: .3rem;
  }

  /* Streamlit 요소 오버라이드 */
  .stTextArea textarea {
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.88rem !important;
    border-radius: 10px !important;
    border: 1px solid #CBD5E1 !important;
    padding: 1rem !important;
    line-height: 1.7 !important;
  }
  .stTextArea textarea:focus {
    border-color: #2C5364 !important;
    box-shadow: 0 0 0 2px rgba(44,83,100,.15) !important;
  }
  .stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1px solid #CBD5E1 !important;
    font-size: 0.86rem !important;
  }
  .stButton > button {
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: .65rem 1.4rem !important;
    font-size: 0.88rem !important;
    background: linear-gradient(135deg, #203A43, #2C5364) !important;
    color: white !important;
    border: none !important;
    transition: all .2s ease !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(44,83,100,.3) !important;
  }
  #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 의존성 & 캐싱
# ──────────────────────────────────────────────
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from google import genai


@st.cache_resource(show_spinner="임베딩 모델을 불러오는 중입니다…")
def load_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


@st.cache_resource(show_spinner="법률 벡터 DB를 구축하는 중입니다…")
def load_vector_db(_embedding_model):
    BASE_DIR = Path(".")
    DATA_DIR = BASE_DIR / "data"
    DB_DIR = str(BASE_DIR / "db" / "faiss_db")

    if Path(DB_DIR).exists() and (Path(DB_DIR) / "index.faiss").exists():
        return FAISS.load_local(DB_DIR, _embedding_model, allow_dangerous_deserialization=True)

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        st.error("data/ 폴더에 PDF 파일이 없습니다.")
        st.stop()

    docs = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        loaded_docs = loader.load()
        for doc in loaded_docs:
            doc.metadata["source_file"] = pdf_path.name
        docs.extend(loaded_docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=180,
        separators=["\n\n", "\n", "제", "①", "②", "③", ".", " "],
    )
    chunks = text_splitter.split_documents(docs)

    vector_db = FAISS.from_documents(chunks, _embedding_model)
    vector_db.save_local(DB_DIR)
    return vector_db

# ──────────────────────────────────────────────
# 키워드 탐지
# ──────────────────────────────────────────────
RISK_KEYWORDS = [
    "100% 보장", "무조건 보장", "전액 보장", "원금 보장",
    "누구나 가입", "가입 즉시 보장", "보험료 부담 없음",
    "업계 최고", "최고의 보험", "가장 좋은 보험", "유일한 선택",
    "확실한 보장", "무조건 지급", "전부 지급",
    "걱정 없이", "부담 없이", "공짜", "무료",
    "손해 없음", "절대", "반드시 지급",
]


def keyword_check(ad_text: str) -> list[str]:
    return [kw for kw in RISK_KEYWORDS if kw in ad_text]


# ──────────────────────────────────────────────
# 답변 후처리
# ──────────────────────────────────────────────
def clean_response(text: str) -> str:
    """Gemini 응답에서 마크다운 기호를 모두 제거."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-•]\s*', '  · ', text, flags=re.MULTILINE)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_result_sections(text: str) -> list[tuple[str, str]]:
    """숫자 번호로 시작하는 섹션을 [(제목, 내용)] 리스트로 반환."""
    pattern = r'(\d+)\.\s*(.+?)(?:\n|:\s*)([\s\S]*?)(?=\n\d+\.\s|\Z)'
    matches = re.findall(pattern, text)
    sections = []
    for num, title, body in matches:
        title = title.strip().rstrip(':')
        body = body.strip()
        sections.append((title, body))
    return sections


def get_risk_badge(text: str) -> str:
    t = text.strip()
    if "매우 높음" in t:
        return '<span class="risk-badge risk-severe">매우 높음</span>'
    elif "높음" in t:
        return '<span class="risk-badge risk-high">높음</span>'
    elif "보통" in t:
        return '<span class="risk-badge risk-mid">보통</span>'
    elif "낮음" in t:
        return '<span class="risk-badge risk-low">낮음</span>'
    return f'<span class="risk-badge risk-mid">{t}</span>'


# ──────────────────────────────────────────────
# RAG 검색 + Gemini 호출
# ──────────────────────────────────────────────
def retrieve_context(retriever, query: str) -> str:
    results = retriever.invoke(query)
    blocks = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page", "unknown")
        content = doc.page_content.strip()
        blocks.append(
            f"[참고문서 {i}]\n출처 파일: {source}\n페이지: {page}\n내용:\n{content}"
        )
    return "\n\n".join(blocks)


def check_insurance_ad(retriever, gemini_client, ad_text: str, ad_type: str) -> str:
    detected_keywords = keyword_check(ad_text)

    search_query = (
        "생명보험 광고 심의 기준에 따라 다음 광고 문구의 위험 표현, "
        "소비자 오인 가능성, 보험금 지급조건, 면책사항, 감액기간, "
        f"과장광고, 기만광고 여부를 검토:\n{ad_text}"
    )
    context = retrieve_context(retriever, search_query)

    prompt = f"""너는 생명보험 광고 심의 보조 AI다.
사용자가 입력한 광고 문구를 검토하라.

중요한 원칙:
- 너는 법적 판단을 확정하지 않는다.
- "위법이다"라고 단정하지 말고 "심의 리스크가 있다", "추가 검토가 필요하다"라고 표현한다.
- 반드시 검색된 참고문서에 기반해 판단한다.
- 검색된 참고문서에 근거가 부족하면 "근거 부족 / 추가 자료 검토 필요"라고 말한다.
- 광고 문구의 마케팅 의도는 유지하되, 소비자 오인 가능성을 낮추는 수정안을 제시한다.

출력 형식 규칙:
- 마크다운(**, ##, -, ```)을 절대 사용하지 마라.
- 항목 나열 시 "· " 기호를 사용하라.
- 순수 평문으로만 깔끔하게 작성하라.

[광고 유형]
{ad_type}

[사전 탐지된 위험 키워드]
{detected_keywords}

[광고 문구]
{ad_text}

[검색된 참고문서]
{context}

아래 형식으로 답변하라.

1. 종합 위험도:
낮음 / 보통 / 높음 / 매우 높음 중 하나

2. 문제가 될 수 있는 표현:
표현별로 구체적으로 지적

3. 위험 사유:
소비자 오인 가능성, 허위·과장 가능성, 중요사항 누락 가능성, 보험금 지급조건 오인 가능성 등

4. 관련 기준:
검색된 참고문서의 출처 파일명과 조항명 제시 (확인되지 않는 조항은 지어내지 말 것)

5. 수정 권장 문안:
심의 리스크를 낮춘 대체 문구 제시 (광고 문맥 유지)

6. 추가 확인 필요 사항:
상품 약관, 보장개시일, 면책기간, 감액기간, 지급한도, 갱신형 여부, 필수 안내문구, 준법감시인 최종 검토 여부 등
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


# ──────────────────────────────────────────────
# UI 렌더링
# ──────────────────────────────────────────────

# 헤더
laws = [
    "보험업법", "개인정보 보호법", "금융소비자 보호법",
    "표시·광고의 공정화에 관한 법률", "금융광고 규제 가이드라인",
    "생명보험 광고에 관한 규정", "시행세칙", "정보통신망법",
]
law_tags_html = "".join(f'<span class="law-tag">{l}</span>' for l in laws)

st.markdown(f"""
<div class="app-header">
  <div class="badge">LINA Life Insurance X Young Makers (TEAM 5)</div>
  <h1>🛡️ 생명보험 광고 RAG 심의 보조 및 추천 광고 카피 제안 도구</h1>
  <p>광고 문구를 입력하면 관련 법령 및 심의기준을 검색하여
     리스크 분석, 문제 표현 지적, 수정 권장안을 제시합니다.</p>
  <div class="law-tags">{law_tags_html}</div>
</div>
""", unsafe_allow_html=True)

# 모델 & DB 로딩
embedding_model = load_embedding_model()
vector_db = load_vector_db(embedding_model)
retriever = vector_db.as_retriever(search_kwargs={"k": 6})

# API Key — Secrets에서 자동 로드, 없으면 직접 입력
gemini_key = st.secrets.get("GEMINI_API_KEY", "")
if not gemini_key:
    st.markdown('<div class="api-section"><div class="label">🔑 API 연결</div></div>', unsafe_allow_html=True)
    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Google AI Studio에서 발급받은 키를 붙여넣으세요",
        label_visibility="collapsed",
    )

# 입력 영역
col_type, _ = st.columns([1, 2])
with col_type:
    ad_type = st.selectbox(
        "광고 유형",
        ["SNS 카드뉴스", "랜딩페이지", "블로그/콘텐츠",
         "문자/카카오톡 광고", "이메일 광고", "영상 광고", "기타"],
        label_visibility="collapsed",
    )

ad_text = st.text_area(
    "광고 문구",
    height=200,
    placeholder="검토할 광고 문구를 여기에 입력하세요.\n\n예시: 암 진단 시 치료비 걱정 없이 100% 보장받으세요. 지금 가입하면 보험료 부담 없이 가족을 지킬 수 있습니다.",
    label_visibility="collapsed",
)

submit = st.button("심의 리스크 검토", type="primary", use_container_width=True)

# ──────────────────────────────────────────────
# 결과 출력
# ──────────────────────────────────────────────
if submit:
    if not gemini_key:
        st.warning("Gemini API Key를 먼저 입력해 주세요.")
        st.stop()
    if not ad_text.strip():
        st.warning("광고 문구를 입력해 주세요.")
        st.stop()

    detected = keyword_check(ad_text)
    if detected:
        kw_html = "".join(f'<span class="kw">{k}</span>' for k in detected)
        st.markdown(f"""
        <div class="keyword-alert">
          <div class="title">사전 탐지된 위험 키워드</div>
          <div>{kw_html}</div>
        </div>
        """, unsafe_allow_html=True)

    gemini_client = genai.Client(api_key=gemini_key)

    with st.spinner("법률 문서를 검색하고 분석하는 중입니다…"):
        try:
            raw = check_insurance_ad(retriever, gemini_client, ad_text, ad_type)
            cleaned = clean_response(raw)
            sections = parse_result_sections(cleaned)

            if sections:
                first_title, first_body = sections[0]
                risk_html = get_risk_badge(first_body)
                st.markdown(f"""
                <div class="result-card">
                  <div class="section-title">{first_title}</div>
                  {risk_html}
                </div>
                """, unsafe_allow_html=True)

                for title, body in sections[1:]:
                    safe_body = body.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    st.markdown(f"""
                    <div class="result-card">
                      <div class="section-title">{title}</div>
                      <div class="content">{safe_body}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                safe = cleaned.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                st.markdown(f"""
                <div class="result-card">
                  <div class="section-title">검토 결과</div>
                  <div class="content">{safe}</div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 면책
st.markdown("""
<div class="disclaimer">
  본 시스템은 컨텐츠 제작 단계의 1차 검토 보조 도구이며, 최종 법적 판단을 대체하지 않습니다.
  실제 광고 집행 전 반드시 준법감시인 또는 광고심의 담당자의 최종 검토를 받으시기 바랍니다.
</div>
""", unsafe_allow_html=True)
