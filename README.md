# 🚢 Real-Time Maritime Logistics Lakehouse (2026)

## 📌 Project Overview
An end-to-end, real-time spatial Data Engineering pipeline processing AIS (Automatic Identification System) maritime telemetry. The project implements a modern **Medallion Lakehouse Architecture** on Microsoft Azure, focusing on **Zero Trust security**, serverless ingestion, and spatial analytics using Uber's H3 indexing.

## 🏗️ Architecture & Data Flow
The pipeline decouples high-throughput data ingestion from analytical processing using a robust event-driven architecture:

1. **Data Source:** Real-time maritime telemetry (JSON) via external WebSocket API (Aisstream.io).
2. **Ingestion (Serverless):** `Azure Functions` (Python) continuously listens to the WebSocket and produces events.
3. **Event Streaming:** `Azure Event Hubs` (Kafka API) acts as a high-throughput memory buffer, decoupling ingestion from the compute layer.
4. **Processing (Bronze/Silver/Gold):** `Azure Databricks` (PySpark / SQL) consumes the Kafka stream (Micro-batching via Databricks Workflows) and processes data through the Medallion architecture.
5. **Storage:** `Azure Data Lake Storage Gen2` (ADLS Gen2) using Delta Lake format.
6. **Governance:** `Databricks Unity Catalog` enforcing strict data governance and table management.

## 🔐 Security & "Zero Trust" Implementation
A core focus of this project is enterprise-grade security, completely eliminating hardcoded secrets:
* **CI/CD Deployment:** Automated deployments via `GitHub Actions` using **OIDC (OpenID Connect)** and Federated Identity Credentials. No deployment profiles or passwords are stored in GitHub.
* **Storage Access:** Databricks connects to ADLS Gen2 using a **System-Assigned Managed Identity** (Access Connector for Azure Databricks) directly integrated into Unity Catalog External Locations.

## 🚀 Project Roadmap & Status

- [x] **Phase 1: Cloud-Native Infrastructure & Data Producers** (Azure Functions, Event Hubs, OIDC CI/CD)
- [x] **Phase 2: Bronze Layer** (Structured Streaming, Kafka API, Unity Catalog Setup, ADLS Gen2)
- [ ] **Phase 3: Silver Layer** (JSON unnesting, H3 Spatial Engineering, World Port Index batch join)
- [ ] **Phase 4: Gold Layer** (Business Aggregations, ACID MERGE INTO operations, Traffic metrics)
- [ ] **Phase 5: Orchestration & Governance** (Databricks Workflows, Repos, Column-Level Security)
- [ ] **Phase 6: Serving & BI** (Power BI / Tableau integration via Databricks SQL)

## 🛠️ Tech Stack
* **Cloud Provider:** Microsoft Azure
* **Compute:** Azure Databricks, Azure Functions (Serverless)
* **Storage & Messaging:** ADLS Gen2, Azure Event Hubs
* **Data Processing:** PySpark (Structured Streaming), Databricks SQL
* **Data Formats:** Delta Lake, JSON
* **Governance:** Unity Catalog
* **CI/CD:** GitHub Actions
