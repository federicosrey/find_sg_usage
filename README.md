# 🔍 AWS Security Group Usage Finder

A Python 3 script to **find all AWS resources associated with a given Security Group (SG)**.  
Useful for **audits**, **security reviews**, and **cleanups** across large AWS environments.

---

## 🚀 Overview

This tool queries multiple AWS services and lists every resource referencing the provided **Security Group ID**.  
It supports a wide range of services commonly managed within enterprise AWS environments.

---

## 🧩 Supported AWS Services

The script currently checks for SG associations across the following services:

| Service | Description |
|----------|--------------|
| **EC2 Instances** | Lists EC2 instances where the SG is attached to any network interface. |
| **ENIs (Elastic Network Interfaces)** | Finds all standalone ENIs using the specified SG. |
| **RDS Instances** | Identifies RDS instances with the SG applied to their network configuration. |
| **DocumentDB Clusters** | Detects MongoDB-compatible DocumentDB clusters referencing the SG. |
| **ElastiCache Clusters** | Checks Redis/Memcached clusters linked to the SG. |
| **OpenSearch Domains** | Finds OpenSearch/Elasticsearch domains associated with the SG. |
| **ELBv2 Load Balancers** | Includes both Application (ALB) and Network (NLB) load balancers. |
| **ECS Services** | Identifies ECS services that use the SG via their task definitions or networking mode. |
| **EKS Clusters** | Checks EKS clusters configured with the SG in their control plane or node groups. |
| **Redshift Clusters** | Lists Redshift clusters where the SG is part of the VPC security group list. |
| **EMR Clusters** | Finds EMR clusters (Hadoop/Spark) referencing the SG. |
| **Elastic Beanstalk Environments** | Identifies Beanstalk environments linked to the SG. |
| **SageMaker Endpoints** | Lists endpoints in SageMaker using the SG for inference or notebook instances. |
| **AWS Batch Compute Environments** | Detects compute environments in AWS Batch tied to the SG. |
| **Glue Connections** | Lists Glue data connections that use the SG for data access. |

If the SG is not found in any service, the script clearly reports that no associations were detected.

---

## 🧠 Prerequisites

### System Requirements
- **Python 3.8+** (tested up to Python 3.12)
- **pip** (latest recommended)

### Python Dependencies
Install required packages:
```bash
pip install boto3 botocore

