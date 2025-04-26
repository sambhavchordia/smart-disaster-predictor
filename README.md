# **Smart Disaster Predictor**  
_Disaster Risk Prediction and Real-time SMS Alert System_  

---

## **Overview**
Smart Disaster Predictor is a machine learning-powered web application that predicts the risk of **floods** and **earthquakes** based on user inputs.  
It sends **instant SMS alerts** using **AWS SNS** when a high-risk event is detected.

The app is deployed on **AWS EC2** behind an **Application Load Balancer (ALB)** for high availability and scalability.

---

## **Features**
- 🌊 Predict Flood Risk (Random Forest, Logistic Regression)
- 🌍 Predict Earthquake Risk (Random Forest, Logistic Regression)
- 📲 Send real-time SMS Alerts through AWS SNS
- ⚡ Deployed on AWS EC2 with IAM Role for secure permissions
- 🌐 Load Balanced deployment using Application Load Balancer (ALB)
- 🖥️ Clean and responsive Streamlit-based web interface

---

## **Tech Stack**
- **Frontend**: Streamlit
- **Backend**: Python (scikit-learn, joblib, boto3)
- **Machine Learning**: Random Forest, Logistic Regression
- **Cloud Services**:
  - AWS EC2 (Compute)
  - AWS SNS (SMS Notification Service)
  - AWS IAM (Secure Credentials)
  - AWS ALB (Load Balancer)
- **Version Control**: Git + GitHub

---

## **Project Structure**
```
smart-disaster-predictor/
│
├── app.py                  # Main Streamlit Application
├── models/                  # Saved Machine Learning Models
│   ├── flood_rf_model.pkl
│   ├── flood_lr_model.pkl
│   ├── earthquake_rf_model.pkl
│   └── earthquake_lr_model.pkl
├── requirements.txt         # Python Dependencies
├── README.md                 # Project Documentation
└── (Optional supporting files)
```

---

# 🚀 **Setup and Installation**

---

## 1. Clone the Repository
```bash
git clone https://github.com/sambhavchordia/smart-disaster-predictor.git
cd smart-disaster-predictor
```

---

## 2. Install Required Packages
```bash
pip install -r requirements.txt
```
This installs:
- streamlit
- scikit-learn
- joblib
- boto3
- numpy

---

## 3. AWS SNS Configuration (for SMS alerts)

✅ **Create an AWS Account** (if not already).

✅ **Set up SNS (Simple Notification Service):**
- Go to AWS Console → SNS → Create a topic (optional for mass alerts).
- Or directly use **Publish to Phone Number** feature.

✅ **IAM Role Setup:**
- Create a Role with **AmazonSNSFullAccess** policy.
- Attach this IAM role to your EC2 instance.
- This allows publishing SMS from your app securely without hardcoded AWS credentials.

✅ **Important:**  
In app.py:
```python
sns = boto3.client('sns', region_name='ap-south-1')
```
No need to write Access Key or Secret if using IAM Role!

✅ **Phone number format:**
Always provide phone number in **E.164 format** (e.g., `+917012345678`).

---

## 4. Streamlit App Configuration

✅ **If testing locally**, run:
```bash
streamlit run app.py
```

✅ **If deploying on EC2**, make sure you expose port `8501`.

✅ Startup commands for EC2:
```bash
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

✅ In your browser:
```
http://<EC2-Public-IP>:8501
```

---

## 5. GitHub Integration
✅ After cloning locally:
```bash
git init
git add .
git commit -m "Initial Commit"
git remote add origin https://github.com/your-username/smart-disaster-predictor.git
git push -u origin main
```

---

## 6. EC2 Deployment

✅ Launch EC2 instance (Amazon Linux 2 or Ubuntu 22.04 preferred).  
✅ Install:
```bash
sudo yum update -y
sudo yum install python3-pip -y
pip3 install streamlit boto3 joblib scikit-learn numpy
```
✅ Clone your GitHub repo on EC2:
```bash
git clone https://github.com/your-username/smart-disaster-predictor.git
```
✅ Start the Streamlit server as mentioned.

✅ Allow **Port 8501** in EC2 Security Group!

---

## 7. Load Balancer Setup (AWS ALB)

✅ Create an **Application Load Balancer (ALB)**:
- Internet-facing
- HTTP Port 80

✅ Create a **Target Group**:
- Protocol: HTTP
- Port: 8501
- Register your EC2 instances

✅ Attach the Load Balancer to the Target Group.

✅ Access your app via:
```
http://<ALB-DNS-Name>
```

---

# 📋 **Usage Instructions**

1. Open the web app.
2. Enter environmental parameters for flood/earthquake.
3. Choose ML model (Random Forest or Logistic Regression).
4. Click on "Predict Risk" → view results immediately.
5. If High Risk → automatic SMS Alert sent to the entered phone number!

---

# ✅ Extra Notes:
- Prefer using IAM roles for production, not hardcoding AWS credentials.
- Move to SNS Production mode for unrestricted SMS sending.
- You can add Auto Scaling to handle sudden traffic spikes.

---

# 📂 Requirements.txt

Inside project:

```
streamlit==1.33.0
scikit-learn==1.4.1
numpy==1.26.4
boto3==1.34.82
joblib==1.4.0
```

