import os
import json
import logging
import traceback
from collections import defaultdict
from flask import Flask, request, jsonify, render_template
from functools import wraps

app = Flask(__name__)
app.url_map.strict_slashes = False
logging.basicConfig(level=logging.INFO)

AI_EXTRACT_DATA = os.getenv("AI_EXTRACT_DATA", "/tmp/data.json")
API_KEY = os.getenv("API_KEY")

def _ensure_store():
  """Create a valid JSON list file if missing or invalid."""
  try:
    if not os.path.exists(AI_EXTRACT_DATA):
      with open(AI_EXTRACT_DATA, "w", encoding="utf-8") as f:
        json.dump([], f)
      return
    with open(AI_EXTRACT_DATA, "r", encoding="utf-8") as f:
      json.load(f)
  except Exception:
    with open(AI_EXTRACT_DATA, "w", encoding="utf-8") as f:
      json.dump([], f)

def _load_events():
  _ensure_store()
  with open(AI_EXTRACT_DATA, "r", encoding="utf-8") as f:
    return json.load(f)

def _save_events(items):
  with open(AI_EXTRACT_DATA, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

def append_call_data(item: dict):
  items = _load_events()
  items.append(item)
  _save_events(items)

def require_api_key(view):
  @wraps(view)
  def wrapped(*args, **kwargs):
    key = request.headers.get("X-API-Key") or (
      (request.headers.get("Authorization") or "").replace("Bearer ", "").strip()
    )
    if not API_KEY or key != API_KEY:
      return jsonify({"error": "unauthorized"}), 401
    return view(*args, **kwargs)
  return wrapped

_ensure_store()

@app.route("/", methods=["GET"])
def home():
  return render_template("homepage.html")

@app.route("/data", methods=["POST"])
@require_api_key
def handle_post():
  data = request.get_json(silent=True) or {}
  append_call_data(data)
  items = _load_events()
  return jsonify({"message": "POST Success", "count": len(items), "data": data}), 201

@app.route("/clear", methods=["POST"])
@require_api_key
def clear_data():
  _save_events([])
  return jsonify({"message": "Existing data cleared"}), 200

# (Optional) Seed a few demo events
@app.route("/seed", methods=["GET"])
def seed():
    samples = [
        {"mc_number":"11111","origin":"San Ramon, CA","destination":"Fort Worth, TX",
         "classification":"deal_success","start_rate":3900,"sold_rate":4200,"reasoning":"Accepted"},
        {"mc_number":"22222","origin":"Oakland, CA","destination":"Dallas, TX",
         "classification":"deal_success","start_rate":6500,"sold_rate":7200,"reasoning":"Matched need"},
        {"mc_number":"33333","origin":"Los Angeles, CA","destination":"Seattle, WA",
         "classification":"deal_success","start_rate":2900,"sold_rate":2900,"reasoning":"Booked at ask"},
        {"mc_number":"44444","origin":"San Francisco, CA","destination":"Dallas, TX",
         "classification":"deal_failure","reasoning":"Rate mismatch"},
    ]
    items = _load_events()
    items.extend(samples)
    _save_events(items)
    return jsonify({"message": "seeded", "count": len(items)}), 201

@app.route("/dashboard", methods=["GET"])
def dashboard():
  data = _load_events()
  total_calls = len(data)
  success_count = 0
  pickup_locations = defaultdict(int)
  dropoff_locations = defaultdict(int)
  failures = defaultdict(int)
  ongoing_count = 0
  rates = []
  sold_rate = 0.0

  for item in data:
    cls = (item or {}).get("classification")
    print(cls)
    if cls == "deal_success":
      success_count += 1
      pickup = item.get("origin")
      dest = item.get("destination")
      start_rate = int(item.get("start_rate")) if item.get("start_rate") else 0
      final_rate = int(item.get("final_rate")) if item.get("final_rate") else 0
      sold_rate += final_rate / start_rate if start_rate != 0 else 0.0
      
      if pickup:
        pickup_locations[pickup] += 1
      if dest:
        dropoff_locations[dest] += 1
      if start_rate and final_rate:
        rates.append([start_rate, final_rate])
    elif cls == "deal_ongoing":
      ongoing_count += 1
    else:
      failures[cls] += 1

  success_rate = (success_count / total_calls * 100.0) if total_calls else 0.0
  sold_rate = ((sold_rate / success_count) * 100) - 100 if success_count != 0 and sold_rate != 0 else 0.0
  fail_count = sum(failures.values())

  pickups_list = [{"location": loc, "count": cnt} for loc, cnt in pickup_locations.items()]
  dropoffs_list = [{"location": loc, "count": cnt} for loc, cnt in dropoff_locations.items()]
  last5_rates_list = [
    {"start_rate": pair[0], "final_rate": pair[1]} for pair in rates
  ]
  unsuccessful_reasons_list = [
    {"reason": reason, "count": cnt} for reason, cnt in failures.items()
  ]

  return render_template(
    "dashboard.html",
    total_calls=total_calls,
    success_count=success_count,
    fail_count=fail_count,
    ongoing_count=ongoing_count,
    success_rate=success_rate,
    pickups=pickups_list,
    dropoffs=dropoffs_list,
    last5_rates=last5_rates_list,
    negotiation_under_pct=sold_rate,
    unsuccessful_reasons=unsuccessful_reasons_list
  )

if __name__ == "__main__":
  port = int(os.getenv("PORT", "8000"))
  app.run(host="0.0.0.0", port=port, debug=True)
