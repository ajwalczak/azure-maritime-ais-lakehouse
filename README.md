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
- [x] **Phase 2: Bronze Layer** (Structured Streaming, Kafka API, Micro-batching via `availableNow=True`)
- [x] **Phase 3: Silver Layer** (JSON unnesting, H3 Spatial Engineering, SCD Type 1 via MERGE INTO)
- [x] **Phase 4: Gold Layer** (Business Aggregations, Daily Port Traffic metrics)
- [x] **Phase 5: Orchestration & Governance** (Databricks Workflows DAG, modular pipelines)
- [ ] **Phase 6: Serving & BI** (Power BI integration via Databricks SQL Warehouse)

## ⚙️ Pipeline Orchestration (Databricks Workflows)
The data pipeline is fully automated using **Databricks Workflows**, forming a robust Directed Acyclic Graph (DAG) for cost-effective micro-batching:

1. **`Ingest_EventHubs_to_Bronze`**: Streams raw JSON payloads from Event Hubs into ADLS Gen2 using `Trigger(availableNow=True)`.
2. **`Process_Silver_Cleaned`**: Unnests JSON payloads and enriches geographical coordinates with **Uber H3** spatial indexes.
3. **Parallel Execution**:
   - **`Update_Silver_Current_State`**: Applies SCD Type 1 logic (`MERGE INTO`) to maintain a deduplicated, real-time snapshot of vessel positions.
   - **`Calculate_Gold_Metrics`**: Aggregates daily KPIs (unique ships per port vicinity) for BI consumption.
## 🛠️ Tech Stack
* **Cloud Provider:** Microsoft Azure
* **Compute:** Azure Databricks, Azure Functions (Serverless)
* **Storage & Messaging:** ADLS Gen2, Azure Event Hubs
* **Data Processing:** PySpark (Structured Streaming), Databricks SQL
* **Data Formats:** Delta Lake, JSON
* **Governance:** Unity Catalog
* **CI/CD:** GitHub Actions
