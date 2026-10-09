from news_analyzer import validate_evidence

news_text = "매출이 전년 동기 대비 15% 증가했다."

report = {
    "positive_factors": [
        {
            "interpretation": "매출이 성장했다.",
            "evidence": "매출이 전년 동기 대비 15% 증가했다.",
        }
    ],
    "negative_factors": [],
}

# 원문과 일치하는 근거 확인
validate_evidence(report, news_text)
print("원문과 일치하는 근거: 통과")

# 근거의 숫자를 일부러 변경
report["positive_factors"][0]["evidence"] = (
    "매출이 전년 동기 대비 50% 증가했다."
)

try:
    validate_evidence(report, news_text)
except ValueError as error:
    print(f"잘못된 근거: 차단 — {error}")
else:
    raise AssertionError("잘못된 근거를 차단하지 못했습니다.")