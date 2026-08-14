# 🤖 AI Business Anomaly Detection & Alert Agent

An AI-powered business monitoring system that analyzes business data, detects abnormal patterns, assigns severity levels, uses a local Llama 3.2 model to generate business insights, creates reports, sends email alerts for critical incidents, and maintains alert history to prevent duplicate notifications.

---

## 📌 Project Overview

Businesses generate large amounts of operational data every day. Manually monitoring this data for unusual changes can be time-consuming and error-prone.

This project automates that process.

The system reads business data from an Excel file and performs:

- 📊 Anomaly detection
- ⚠️ Severity classification
- 🔗 Incident grouping
- 🤖 AI-powered business analysis
- 📄 Automated business report generation
- 📧 Email alerts for high-severity incidents
- 📝 Alert history tracking
- 🛡️ Duplicate alert protection

---

## 🚀 Key Features

### 1. 📊 Anomaly Detection

The system analyzes business metrics and identifies unusual changes from their expected baseline.

Detected anomalies include information such as:

- Date
- Metric
- Actual value
- Baseline value
- Percentage change
- Z-score
- Direction of change

---

### 2. ⚠️ Severity Engine

Every detected anomaly is assigned a severity level:

| Severity | Action |
|---|---|
| 🟢 LOW | No email |
| 🟡 MEDIUM | No email |
| 🔴 HIGH | Email alert |
| 🚨 CRITICAL | Email alert |

---

### 3. 🔗 Incident Grouping

Multiple anomalies occurring on the same date are grouped into a single business incident.

Example:

```text
Revenue anomaly
Orders anomaly
Traffic anomaly
        ↓
   INC-001

   4. 🤖 AI Business Analysis

The project uses Llama 3.2 through Ollama to analyze detected incidents locally.

The AI generates:

Business Insight
Possible Cause
Business Impact
Recommended Action

Example:

BUSINESS INSIGHT:
Revenue increased significantly compared to the baseline.


POSSIBLE CAUSE:
Possible increase in demand or successful marketing activity.


BUSINESS IMPACT:
The increase may indicate a positive business opportunity.


RECOMMENDED ACTION:
Investigate the reason for the increase and monitor future revenue.
5. 📄 Automated Business Reports

After analyzing incidents, the system automatically generates a report containing:

Total anomalies
Total incidents
Incident details
AI-generated business analysis
Severity information

Reports are saved inside:

reports/

Example:

AI_Business_Report_20260815_002516.txt
6. 📧 Automatic Email Alerts

The system uses Resend to send email notifications.

Email alerts are triggered only for:

🔴 HIGH
🚨 CRITICAL

LOW and MEDIUM incidents do not generate emails.

7. 📝 Alert History

Every successfully sent alert is recorded in:

reports/alert_history.csv

The history stores information such as:

Incident ID
Date
Severity
Metrics
Email status
Email ID
Sent timestamp

This provides an audit trail of previously sent alerts.

8. 🛡️ Duplicate Alert Protection

Before sending a HIGH or CRITICAL alert, the system checks the alert history.

Incident detected
       ↓
Is severity HIGH/CRITICAL?
       ↓
      YES
       ↓
Check alert_history.csv
       ↓
Already sent?
    ↙       ↘
  YES        NO
   ↓          ↓
 SKIP       SEND
              ↓
       Save history

This prevents the same incident from generating repeated emails.

🏗️ Project Architecture
                 Business Excel Data
                         │
                         ▼
                ┌─────────────────┐
                │ Data Processing │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Anomaly      │
                │    Detection    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Severity Engine │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Incident     │
                │    Grouping     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Llama 3.2 AI  │
                │    Analysis     │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Business Report         Severity Check
                                    │
                           ┌────────┴────────┐
                           ▼                 ▼
                       LOW/MEDIUM       HIGH/CRITICAL
                           │                 │
                        No Email             ▼
                                      Alert History
                                           │
                                  ┌────────┴────────┐
                                  ▼                 ▼
                              Already Sent       New Alert
                                  │                 │
                                Skip              Email
                                                    │
                                                    ▼
                                             Save History
🛠️ Tech Stack
Programming
Python
Data Processing
Pandas
OpenPyXL
AI
Ollama
Llama 3.2
Email
Resend API
Configuration
Python Dotenv
.env
Data Source
Excel (.xlsx)
Output
TXT business reports
CSV alert history
Email notifications
📁 Project Structure
AI Business Anomaly Detection & Alert Agent/
│
├── .env
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   └── raw/
│       └── business_data.xlsx
│
├── reports/
│   ├── AI_Business_Report_....txt
│   └── alert_history.csv
│
└── src/
    ├── __init__.py
    │
    ├── ai_business_report.py
    ├── ai_explainer.py
    ├── Anomaly_detector.py
    ├── Severity_engine.py
    ├── incident_grouper.py
    │
    ├── alert_engine.py
    ├── alert_history.py
    ├── email_alert.py
    │
    ├── data_loader.py
    ├── data_validator.py
    ├── cross_metric_analyzer.py
    ├── business_explainer.py
    └── generate_data.py
⚙️ Installation
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
2. Open the project
cd "AI Business Anomaly Detection & Alert Agent"
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
Windows PowerShell
.\venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
🤖 Ollama Setup

Install Ollama and make sure the Llama 3.2 model is available.

Check installed models:

ollama list

Run the model if required:

ollama run llama3.2

The project uses the local Llama model for business anomaly analysis.

🔐 Environment Variables

Create a .env file in the project root.

Example:

RESEND_API_KEY=your_resend_api_key
FROM_EMAIL=your_verified_sender_email
TO_EMAIL=your_destination_email

Do not upload your real .env file to GitHub.

The .gitignore file already excludes:

.env
▶️ Running the Project

From the project root:

python -m src.ai_business_report

The system will:

1. Load business data
2. Detect anomalies
3. Calculate severity
4. Group incidents
5. Analyze incidents using Llama 3.2
6. Generate business insights
7. Generate the business report
8. Check alert history
9. Send HIGH/CRITICAL email alerts
10. Record sent alerts
11. Prevent duplicate alerts
📊 Example Output
📂 Loading business data...
✅ Excel file loaded successfully!


🔍 Detecting anomalies...
✅ 37 anomalies detected.


⚠️ Calculating severity...
✅ Severity calculated.


🔗 Grouping incidents...
✅ Incident grouping completed.


📊 Total incidents found: 32


🚀 Starting full AI business analysis + automatic alerts...


🤖 [1/32] Analyzing INC-001 with Llama 3.2...
✅ INC-001 analysis completed.


📧 HIGH severity detected!
🚀 Sending email alert for INC-001...
✅ Email alert sent for INC-001!

Final output:

🎉 AI BUSINESS ANALYSIS + ALERTS COMPLETED


📊 Total anomalies : 37
📊 Total incidents : 32


📄 Complete report saved at:
reports/AI_Business_Report_YYYYMMDD_HHMMSS.txt
📧 Alert Rules
🟢 LOW
   → No email


🟡 MEDIUM
   → No email


🔴 HIGH
   → Email alert


🚨 CRITICAL
   → Email alert
🛡️ Duplicate Protection

The system checks alert_history.csv before sending an alert.

If an incident has already generated an alert:

🚫 Email already sent for INC-001.
⏭️ Skipping duplicate alert.

This prevents unnecessary repeated notifications.

📈 Current Test Results

The complete pipeline has been tested with:

Total anomalies    : 37
Total incidents    : 32
AI analysis        : Completed
Email integration  : Completed
Alert history      : Completed
Duplicate blocking : Verified

🔮 Future Improvements

Possible future enhancements include:

📊 Power BI dashboard integration
📈 Real-time business monitoring
🗄️ Database storage instead of CSV
🌐 Web dashboard
📧 HTML email templates
⏰ Scheduled automatic execution
☁️ Cloud deployment
📱 Slack/Teams notifications
📊 Advanced anomaly detection models
🔄 Automated daily/weekly reports
🎯 Learning Outcomes

This project demonstrates practical experience with:

Python
Pandas
Excel data processing
Anomaly detection
Statistical analysis
AI/LLM integration
Ollama
API integration
Email automation
Incident management
Alert systems
Environment variables
File-based logging
Automation pipelines
👨‍💻 Author

Tanmay Pandey

B.Tech Student | Data Analytics & AI Enthusiast

⭐ Project Goal

The goal of this project is to demonstrate how AI can be combined with traditional data analytics to automatically identify unusual business behavior, explain what may have happened, assess the potential business impact, and notify stakeholders when immediate attention is required.