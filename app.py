import requests
from discord_notifier import send_discord
from report_formatter import format_report

import streamlit as st
from google.genai import errors
from news_analyzer import analyze_news, MODEL_NAME, ANALYSIS_VERSION
from analysis_store import save_analysis

st.set_page_config(page_title="AI 기업 뉴스 분석")

st.title("AI 기업 뉴스 분석")
st.caption("입력한 자료를 바탕으로 사실, 해석, 불확실성을 정리합니다.")

# 처음 화면을 열었을 때 저장 공간 준비
if "report" not in st.session_state:
    st.session_state["report"] = None
    st.session_state["source"] = ""

if "discord_sent" not in st.session_state:
    st.session_state["discord_sent"] = False

with st.form("news_form"):
    news_text = st.text_area(
        "분석할 뉴스 본문",
        height=220,
        placeholder="뉴스 또는 기업 발표 내용을 붙여 넣으세요.",
    )
    submitted = st.form_submit_button("분석하기")

if submitted:
    st.session_state["discord_sent"] = False
    st.session_state["report"] = None
    st.session_state["source"] = ""

    if not news_text.strip():
        st.warning("분석할 본문을 입력해주세요.")
    else:
        try:
            with st.spinner("뉴스를 분석하고 있습니다…"):
                report = analyze_news(news_text)

        except ValueError as error:
            st.error(str(error))

        except errors.APIError as error:
            if error.code == 503:
                st.error("AI 서버가 혼잡합니다. 잠시 후 다시 시도해주세요.")
            else:
                st.error(f"AI 요청에 실패했습니다. 오류 코드: {error.code}")

        else:
            st.session_state["report"] = report
            st.session_state["source"] = news_text

            try:
                save_analysis(
                    news_text,
                    report,
                    MODEL_NAME,
                    ANALYSIS_VERSION,
                )
            except OSError:
                st.warning(
                    "분석은 완료됐지만 기록을 저장하지 못했습니다. "
                    "폴더의 쓰기 권한과 저장 공간을 확인해주세요."
                )

# 버튼을 누른 순간뿐 아니라 저장된 결과가 있으면 표시
if st.session_state["report"] is not None:
    report = st.session_state["report"]

    st.success("분석이 완료됐습니다.")

    if st.checkbox("분석에 사용한 원문 보기"):
        st.text(st.session_state["source"])

    st.subheader("핵심 사실")
    for fact in report["facts"]:
        st.write(f"• {fact}")

    st.subheader("긍정 요인")
    if not report["positive_factors"]:
        st.write("자료에서 확인된 긍정 요인이 없습니다.")
    for factor in report["positive_factors"]:
        st.write(f"해석: {factor['interpretation']}")
        st.write(f"근거: {factor['evidence']}")

    st.subheader("부정 요인")
    if not report["negative_factors"]:
        st.write("자료에서 확인된 부정 요인이 없습니다.")
    for factor in report["negative_factors"]:
        st.write(f"해석: {factor['interpretation']}")
        st.write(f"근거: {factor['evidence']}")

    st.subheader("불확실한 부분")
    for item in report["uncertainties"]:
        st.write(f"• {item}")

    st.caption(
        "결과는 마지막으로 분석한 원문을 기준으로 합니다. "
        "근거 인용의 원문 포함 여부를 검사했으며, "
        "해석의 타당성과 누락된 정보는 직접 확인해주세요."
    )

if st.session_state["report"] is not None:
    if st.session_state["discord_sent"]:
        st.success("이 분석 결과를 디스코드로 전송했습니다.")

    if st.button(
        "디스코드로 보내기",
        disabled=st.session_state["discord_sent"],
    ):
        message = format_report(st.session_state["report"])

        if len(message) > 2000:
            st.warning("분석 결과가 길어 전송할 수 없습니다. 2,000자 이하가 필요합니다.")
        else:
            try:
                send_discord(message)
            except ValueError as error:
                st.error(str(error))
            except requests.exceptions.RequestException:
                st.error("디스코드 전송에 실패했습니다. 웹훅 설정과 연결을 확인해주세요.")
            else:
                st.session_state["discord_sent"] = True
                st.rerun()