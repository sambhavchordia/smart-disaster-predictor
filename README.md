# **Smart Disaster Predictor**  
_Disaster Risk Prediction and Real-time SMS Alert System_  

---

## **Overview**
Smart Disaster Predictor is a machine learning-powered web application that predicts the risk of **floods** and **earthquakes** based on user inputs.  
It sends **instant SMS alerts** using **AWS SNS** when a high-risk event is detected.

The app is deployed on **AWS EC2** behind an **Application Load Balancer (ALB)** for high availability and scalability.

AWS RDS used for database
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

# **AWS RDS Integration for Smart Disaster Predictor**

This project uses **AWS RDS** (Relational Database Service) to store the **flood and earthquake risk prediction data** submitted by users through the **Streamlit app**. Below are the steps to set up and integrate **AWS RDS** with the project.

---

## **1. Prerequisites**

- **AWS Account**: You need an active AWS account.
- **RDS Instance**: We are using **MySQL** as the database engine.
- **EC2 Instance**: The Streamlit app is hosted on an EC2 instance in the same AWS region.
- **Security Group**: Proper inbound rules for allowing access to the MySQL database.
  
---

## **2. AWS RDS Setup**

### **2.1 Create an RDS MySQL Database Instance**

1. Go to the **AWS Management Console** and search for **RDS**.
2. Click on **Create database**.
3. Select **MySQL** as the database engine.
4. Choose a version of **MySQL** (latest recommended).
5. Set **DB instance class** (e.g., `db.t2.micro` for testing).
6. Set **Master username** and **Password**.
7. Choose **Publicly Accessible** to allow external connections (optional based on the app's requirements).
8. Configure **VPC**, **Security Groups**, and **Subnet** as needed.
9. Finish the setup and click on **Create Database**.

---

### **2.2 Connect to RDS from EC2**

1. **Get the RDS Endpoint**: 
   - Go to **RDS > Databases**.
   - Select your **RDS instance** and find the **Endpoint** under **Connectivity & Security**.
   - It will look something like `smart-disaster-db.c90c2k8see01.ap-south-1.rds.amazonaws.com`.

2. **Configure the EC2 Instance**:
   - Ensure the **EC2 instance** has the correct **IAM role** attached and the **security group** allows access to port `3306` (MySQL).
   - Add an inbound rule for **port 3306** in the **EC2 security group**.

---

## **3. Modify the Streamlit App to Connect to RDS**

In your **Streamlit app**, the database connection is configured like this:

### **Code Example for Connecting to MySQL RDS**

```python
import mysql.connector

# Connect to MySQL RDS database
def connect_to_db():
    db_connection = mysql.connector.connect(
        host="your-rds-endpoint",  # Replace with the actual RDS endpoint
        user="your-username",  # e.g., "admin"
        password="your-password",  # Use the password you set for RDS
        database="disaster_db"  # Name of the database created in RDS
    )
    return db_connection
```

---

## **4. IAM Role Setup for EC2 Access to RDS**

1. Go to **IAM > Roles** in the AWS Console.
2. Create a new **IAM Role** with **AmazonRDSFullAccess** policy attached.
3. Attach this **IAM role** to the **EC2 instance**.

---

## **5. Test the Integration**

- Once everything is configured, start your **Streamlit app** on EC2 and verify that user data is being saved to the **RDS MySQL database**.
- Use **MySQL Workbench** or **command line** to confirm that data is being inserted correctly into your RDS instance.

---

## **6. Conclusion**

By following these steps, you can successfully integrate **AWS RDS** with your **Streamlit app** to store the disaster prediction data in a centralized database. This approach ensures scalability, security, and easy access to data.

---

### **2. Easy Steps to Connect AWS RDS (MySQL) in Simple Language**

---

### **Step 1: Create an RDS Instance**

1. **Log into AWS** and open the **RDS service**.
2. Click on **Create Database** and choose **MySQL** as your database engine.
3. Enter a **username** and **password** for your database.
4. Set **Publicly Accessible** to **Yes** (to allow access from your EC2 instance or local machine).
5. Complete the setup and create the instance.

---

### **Step 2: Get the RDS Endpoint**

1. Go to **RDS** > **Databases**.
2. Click on your database to view details.
3. Copy the **Endpoint URL** (it looks like `your-db-instance-name.cxxivlph1xwy.ap-south-1.rds.amazonaws.com`).

---

### **Step 3: Set Up Security Groups**

1. Go to **EC2** > **Security Groups**.
2. Find the **Security Group** for your **EC2 instance**.
3. Add a new **Inbound Rule** for **port 3306** (MySQL) and set the **Source** to your **IP address** or **Security Group** of your EC2 instance.

---

### **Step 4: Update Streamlit App to Connect to RDS**

1. In the **Streamlit app**, connect to **RDS** using the **mysql-connector**:
   ```python
   import mysql.connector

   def connect_to_db():
       db_connection = mysql.connector.connect(
           host="your-rds-endpoint",  # Replace with your RDS endpoint
           user="your-db-username",  # e.g., "admin"
           password="your-db-password",  # e.g., "password"
           database="disaster_db"  # Name of your database
       )
       return db_connection
   ```
2. Make sure your **MySQL** connection works and data is saved from the app.

---

### **Step 5: Test the Connection**

- Test by entering data in the **Streamlit app** and check your **MySQL database** in **RDS** if the data is getting saved.

---

# 📋 **Usage Instructions**

1. Open the web app.
2. Enter environmental parameters for flood/earthquake.
3. Choose ML model (Random Forest or Logistic Regression).
4. Click on "Predict Risk" → view results immediately.
5. If High Risk → automatic SMS Alert sent to the entered phone number!

