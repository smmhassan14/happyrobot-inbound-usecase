# **Acme Logistics – Inbound Carrier Sales Automation**

## Solution Overview

Inbound carrier calls are one of the most time-consuming yet critical workflows for any freight brokerage. Each call typically involves verifying the carrier, answering a wide range of questions, negotiating rates, and finalizing deals. For brokers, this creates a heavy workload that pulls focus away from revenue-driving conversations.

To help brokerages scale this process, I used the HappyRobot platform to design an AI-powered inbound call automation system.

This solution delivers:

- Fast and consistent carrier verification, eliminating manual bottlenecks.
- Real-time load matching, negotiation, and outcome recording.
- Sales engagement only when a carrier is verified and ready to do business.
- Clear visibility into call outcomes, trends, and performance metrics.
    
This system enables brokerages to handle more calls with greater consistency, freeing sales teams to focus on closing deals while giving leadership sharper visibility into performance.

----------

## Workflow Design

### 1. Inbound Call Trigger

Carriers are connected immediately to the AI agent as soon as they call — no hold times, no bottlenecks.

_In our example workflow, the **Web Call** trigger is used to simulate a live phone call environment._

### 2. AI Inbound Voice Agent Engagement

- Greets carriers in a friendly, professional style that feels natural, not robotic.
- Collects the carrier’s MC number and verifies it automatically through FMCSA API integration.
- Ensures only eligible carriers proceed, improving compliance and trust.
    
### 3. Load Matching & Pitching

- The AI agent retrieves available load opportunities (origin, destination, pickup/delivery windows, equipment type, and rate) from integrated APIs and databases, aligning them with the carrier’s request.  
- When a suitable load is identified, the agent presents the details clearly and professionally, answering any questions along the way.
- The agent then confirms whether the carrier is ready to move forward, creating a natural decision point in the conversation.

### 4. Negotiation Process

- If a carrier pushes back on the rate, the AI agent can manage multiple rounds of back-and-forth negotiation, evaluating each counteroffer against custom business rules set by the brokerage.
- If a deal is reached, the call is seamlessly transferred to a live sales rep to finalize.
- If no deal is reached, the agent can search for alternative loads to keep the conversation moving or politely ends the call, if the carrier requires no further assistance.

### 5. AI Extraction & AI Classify

- The system automatically extracts structured data from every call — including load ID, MC number, starting rate, final rate, and pickup/destination, etc.
- Each call is then classified (`deal_success`, `deal_failure`, `verification_failure`), while carrier sentiment is also captured to support performance tracking and identify at-risk relationships.

### 6. Reporting

- Call outcomes can be passed via webhooks into the brokerage’s existing analytics or reporting systems.  
- Using the structured data from AI extraction, brokers can build real-time dashboards that track inbound activity — including success rates, verification failures, negotiation outcomes, and carrier sentiment — to spot trends, measure performance, and make data-driven decisions that strengthen carrier relationships.

_In our example workflow, reporting is demonstrated through a containerized dashboard environment, deployed using **Docker** and **Google Cloud Run**._

----------

## Metrics & Insights

Our solution doesn’t just handle calls — it generates insights that we can use to improve carrier sales strategy and decision-making:

- **Inbound call volume** – total number of carrier interactions handled.
- **Verification outcomes** – pass/fail rates that highlight compliance trends.
- **Deal success rate (%)** – how many calls yield to booked loads.
- **Failure reasons** – structured visibility into why deals are lost (e.g., rate mismatch, equipment availability, failed verification).
- **Negotiation metrics** – close-to-start ratios to measure pricing effectiveness.
- **Geographic trends** – top pickup and dropoff locations by frequency and success rate.  
- **Carrier sentiment** – positive, neutral, or negative tone indicators to flag relationship risks early.

**Customer Value:** We will be able to gain _actionable intelligence_ — insights into where deals are won, where they’re lost, and what can be done to improve close rates and strengthen carrier relationships.

----------

## Dashboard Deployment & Infrastructure

- **API Layer:** A Flask-based service that accepts call outcome data via a secured `/data` POST endpoint and renders performance metrics at `/dashboard`.  
- **Cloud Deployment:** The entire service is containerized with Docker and deployed on Google Cloud Run - [live dashboard](https://inbound-dashboard-711249339852.us-west2.run.app/).      
- **Security:**  
    - **API key authentication** is required for all write endpoints to prevent unauthorized data submission. The API key is configured within the workflow for secure communication.
    - **HTTPS is automatically enforced** by Cloud Run, ensuring data is securely transmitted end-to-end.
-   **Maintainability:** New code changes can be rolled out with a single `gcloud run deploy` command, creating a new revision while keeping the previous one available for rollback.

----------

## Business Impact for Acme Logistics

- **For Carriers:** A faster, more professional experience with less waiting.
- **For Sales Staff:** Time is spent only on verified, ready-to-close freight carriers, instead of manual checks.
- **For Leadership:** A clear view of inbound sales performance with key performance indicators and trend insights.
- **For the Business:** Increased close rates, improved efficiency, and stronger carrier relationships.
    
----------

## Conclusion

By letting AI handle repetitive steps and surfacing meaningful insights, Acme Logistics can scale inbound carrier sales, empower brokers, and deliver a smoother experience for every carrier interaction.
