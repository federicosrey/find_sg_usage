# 🔍 AWS Security Group Usage Finder

A Python 3 utility to **discover all AWS resources associated with a specific Security Group (SG)**.  
Ideal for **security audits**, **infrastructure cleanup**, or **dependency analysis** in large AWS environments.

---

## 🚀 Overview

This tool queries multiple AWS services and reports every resource referencing the provided **Security Group ID**.  
It supports a wide range of AWS-managed services and provides a concise, human-readable summary of all matches.

If the SG is not found in any service, the script will clearly report that no associations were detected.

---

## 🧩 Supported AWS Services

The script checks for Security Group associations across the following AWS services:

| Service | Description |
|----------|--------------|
| **EC2 Instances** | Lists EC2 instances where the SG is attached to one or more network interfaces. |
| **ENIs (Elastic Network Interfaces)** | Detects standalone ENIs directly using the specified SG. |
| **RDS Instances** | Identifies database instances referencing the SG. |
| **DocumentDB Clusters** | Finds MongoDB-compatible DocumentDB clusters using the SG. |
| **ElastiCache Clusters** | Checks Redis/Memcached clusters associated with the SG. |
| **OpenSearch Domains** | Detects OpenSearch or legacy Elasticsearch domains with the SG attached. |
| **ELBv2 Load Balancers** | Includes both Application (ALB) and Network (NLB) load balancers referencing the SG. |
| **ECS Services** | Finds ECS services using the SG via task networking or service-level configuration. |
| **EKS Clusters** | Detects EKS clusters using the SG in their control plane or node groups. |
| **Redshift Clusters** | Lists Redshift clusters referencing the SG in their VPC configuration. |
| **EMR Clusters** | Finds EMR (Hadoop/Spark) clusters that reference the SG. |
| **Elastic Beanstalk Environments** | Identifies Beanstalk environments linked to the SG. |
| **SageMaker Endpoints** | Lists SageMaker endpoints or notebook instances using the SG. |
| **AWS Batch Compute Environments** | Finds compute environments in AWS Batch tied to the SG. |
| **Glue Connections** | Lists AWS Glue data connections using the SG for network access. |

---

## 🧠 Prerequisites

### System Requirements
- **Python 3.8+** (tested up to Python 3.12)
- **pip** (latest version recommended)
- **AWS credentials** configured locally (see below)

### Python Dependencies

Install dependencies using pip:

```bash
pip install boto3 botocore
```

---

## 🔐 AWS Authentication

The script requires valid AWS credentials to access resources.  
You can authenticate in several ways:

### Option 1 — AWS CLI Configuration (Recommended)
Run the following command and enter your credentials when prompted:
```bash
aws configure
```
This will store your keys and default region under `~/.aws/credentials`.

---

### Option 2 — Environment Variables
You can also export your credentials directly:
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

---

### Option 3 — AWS SSO or IAM Role
If your organization uses AWS SSO or IAM Roles with profiles, make sure your config file (`~/.aws/config`) includes your profile and region.  
You can specify it when running the script:
```bash
AWS_PROFILE=your-profile python find_sg_usage.py
```

---

### 💡 Recommended: Use [`awsprofile`](https://github.com/ivours/awsprofile)
For an automated and streamlined authentication process, consider using the [**awsprofile**](https://github.com/ivours/awsprofile) repository.  
It includes a convenient `.sh` script that handles AWS authentication interactively and sets up environment variables for you.

Example:
```bash
./awsprofile.sh <your-profile>
```
This method is ideal for multi-account environments or when switching between different AWS roles frequently.

---

## ⚙️ Usage

Run the script and enter the **Security Group ID** when prompted:

```bash
python find_sg_usage.py
```

Example prompt:
```
Enter the Security Group ID to search for: sg-0123456789abcdef0
```

The script will query all supported services and output a categorized summary of matches.

---

## 🧾 Example Output

```
Enter the Security Group ID to search for: sg-0a1b2c3d4e5f67890

🔍 Searching for resources associated with Security Group: sg-0a1b2c3d4e5f67890

✅ Found resources:

• EC2 Instances:
  - i-0d7f1a234b567cdef (Name: backend-api-prod)
  - i-0e8a9b123c456def0 (Name: cache-server)

• ENIs:
  - eni-0234abcd5678efgh (attached to EC2 i-0d7f1a234b567cdef)

• RDS Instances:
  - myapp-db-prod

• OpenSearch Domains:
  - analytics-cluster

No associations found in:
DocumentDB, ElastiCache, ECS, EKS, Redshift, EMR, Elastic Beanstalk, SageMaker, AWS Batch, Glue.
```

---

## 🧩 Example Use Cases

- Identify which resources would be impacted if a Security Group were deleted.  
- Detect unused or “orphaned” Security Groups.  
- Audit compliance and networking boundaries for security reviews.  
- Automate SG dependency analysis in large AWS accounts.

---

## 🧰 Development

Clone the repository:

```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
```

Run locally:

```bash
python find_sg_usage.py
```

---

## 🧪 Tested Environments

| OS | Python | AWS SDK |
|----|---------|----------|
| macOS (Apple Silicon) | 3.12 | boto3 1.35+ |
| Ubuntu 22.04 (x86_64) | 3.10 | boto3 1.35+ |
| Amazon Linux 2 | 3.9 | boto3 1.34+ |

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome.  
If you'd like to add support for another AWS service, please open an issue or PR with the relevant boto3 calls.

---

## 🧾 License

Licensed under the **MIT License** — free to use, modify, and distribute with attribution.

---

### 💡 Author
Developed with ❤️ by **Fede Rey** — Cloud / DevOps Engineer.  
_For audits, automation, and keeping your AWS tidy._