import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def save_analysis(news_text, report, model_name, analysis_version):
    history_dir = Path(__file__).resolve().parent / "analysis_history"
    history_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": model_name,
        "analysis_version": analysis_version,
        "source_text": news_text,
        "report": report,
    }

    record_path = history_dir / f"{uuid4().hex}.json"

    record_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return record_path