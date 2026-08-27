#!/usr/bin/env python3
"""
本地/CI 发布辅助脚本。
用法：
  python scripts/publish_daily.py path/to/todays-report.html path/to/todays-data.json

作用：
1. 将当天 HTML 复制为 index.html
2. 保存 archive/YYYY-MM-DD.html
3. 更新 data/latest.json
4. 追加 data/history.json
"""
from pathlib import Path
import sys, json, shutil, datetime

root = Path(__file__).resolve().parents[1]
if len(sys.argv) != 3:
    raise SystemExit("Usage: publish_daily.py TODAY_HTML TODAY_JSON")

html_path = Path(sys.argv[1])
json_path = Path(sys.argv[2])
data = json.loads(json_path.read_text(encoding="utf-8"))
date = data["report_date"]

shutil.copy2(html_path, root / "index.html")
shutil.copy2(html_path, root / "archive" / f"{date}.html")
(root / "data" / "latest.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
)

history_path = root / "data" / "history.json"
history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
history = [x for x in history if x.get("date") != date]
history.append({
    "date": date,
    "updated_at": data.get("updated_at"),
    "href": f"/archive/{date}.html",
    "benchmarks": data.get("tracked_benchmarks", len(data.get("benchmarks", []))),
    "watch_sources": data.get("watch_sources")
})
history.sort(key=lambda x: x["date"])
history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Published {date}")
