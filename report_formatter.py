def format_report(report):
    lines = ["[AI 기업 뉴스 분석]", "", "■ 핵심 사실"]

    for fact in report["facts"]:
        lines.append(f"• {fact}")

    lines.append("\n■ 긍정 요인")
    if not report["positive_factors"]:
        lines.append("확인된 요인 없음")
    for factor in report["positive_factors"]:
        lines.append(f"해석: {factor['interpretation']}")
        lines.append(f"근거: {factor['evidence']}")

    lines.append("\n■ 부정 요인")
    if not report["negative_factors"]:
        lines.append("확인된 요인 없음")
    for factor in report["negative_factors"]:
        lines.append(f"해석: {factor['interpretation']}")
        lines.append(f"근거: {factor['evidence']}")

    lines.append("\n■ 불확실한 부분")
    for item in report["uncertainties"]:
        lines.append(f"• {item}")

    return "\n".join(lines)