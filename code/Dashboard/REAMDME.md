# Acme Logistics – Inbound Call Dashboard

This project demonstrates an **AI-powered inbound carrier call automation** dashboard.  
It tracks carrier calls, success/failure rates, negotiation metrics, and provides a clean web UI built with Flask + TailwindCSS.

The application is containerized using **Docker** and deployed on **Google Cloud Run**.

---

## 🚀 Features

- **Inbound call metrics** (total calls, success/failure, negotiations ongoing, success rate)
- **Rate negotiation insights** (starting vs final rate, sold for % over/under starting rate)
- **Load pickup / dropoff analytics**
- **Recent deal history**
- **Unsuccessful call reasons**
- **Modern UI** (TailwindCSS, dark mode, responsive design)
- **REST API** for programmatic access to call data:
  - `POST /data` → Data extracted from incoming calls on HappyRobot platform
  - `GET /data` → Fetch all records
  - `POST /clear` → Clear stored records

---

## 🌐 WWW

The current deployment is running on **Google Cloud Run** and is accessible here: [https://inbound-dashboard-711249339852.us-west2.run.app/](https://inbound-dashboard-711249339852.us-west2.run.app/)

- Homepage: `/`
- Dashboard: `/dashboard`
- API: `/data`, `/clear`

### Sending extracted data via HappyRobot AI inbound agent

The AI agent is configured to send extracted call data to this website using the API endpoint `/data`. Once sent, the `/dashboard` route displays the processed call metrics in the dashboard.

### Sending data for testing purposes (curl -X POST)

```bash
curl -X POST https://inbound-dashboard-711249339852.us-west2.run.app/data \
  -H "Content-Type: application/json" \
  -H "X-API-Key: d28ddafe3ec9882b270a0acae9c612b374ec1a058edfea6741ed8dcf8ec4398a" \
  -d '{"mc_number": "12345", "destination": "Seattle, TX", "load_id": "1", "classification": "deal_success", "reasoning": "Carrier accepted the final rate.", "origin": "Oakland, CA", "start_rate": "2500", "weight": "5000 lbs", "datetime": "September 20th, 2025 at 12PM", "final_rate": "2580"}'
{"count":1,"data":{"classification":"deal_success","datetime":"September 20th, 2025 at 12PM","destination":"Seattle, TX","final_rate":"2580","load_id":"1","mc_number":"12345","origin":"Oakland, CA","reasoning":"The call resulted in a no deal agreed.","start_rate":"2500","weight":"5000 lbs"},"message":"POST Success"}
```

---

## 🖥 Running Locally

### 🛠 Prerequisites

- Python 3.9+
- Flask
- API Key: `d28ddafe3ec9882b270a0acae9c612b374ec1a058edfea6741ed8dcf8ec4398a`

### Run on localhost:8000

```bash
# Clone repo
git clone https://github.com/smmhassan14/happyrobot-inbound-usecase.git
cd Dashboard

# Set environment variables
export API_KEY="d28ddafe3ec9882b270a0acae9c612b374ec1a058edfea6741ed8dcf8ec4398a"
export PORT=8000

# Run on localhost
python server.py
```

### Send a post request

```bash
# Sending data
curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -H "X-API-Key: d28ddafe3ec9882b270a0acae9c612b374ec1a058edfea6741ed8dcf8ec4398a" \
  -d '{"mc_number": "12345", "destination": "Seattle, TX", "load_id": "1", "classification": "deal_success", "reasoning": "Carrier accepted the final rate.", "origin": "Oakland, CA", "start_rate": "2500", "weight": "5000 lbs", "datetime": "September 20th, 2025 at 12PM", "final_rate": "2580"}'
```

### View dashboard

- http://localhost:8000/dashboard/
