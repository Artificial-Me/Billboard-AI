# Billboard AI: Revolutionizing Outdoor Advertising with Computer Vision & AI

![BillboardAI Image](assets/billboardAI-SD3-5-003.webp?raw=true)

## Overview

Billboard AI is an intelligent platform designed to transform the Outdoor Advertising (OOH) landscape. By deploying smart sensor devices on billboard structures, we capture real-time data on audience engagement and environmental context. This empowers Account Executives (AEs) with precise, actionable insights, moving beyond traditional estimations to data-driven campaign analysis and optimization, ultimately boosting sales effectiveness and demonstrating clear ROI to advertisers.

## The Problem

Traditional OOH advertising relies heavily on estimated impression data based on generalized traffic counts and demographic assumptions. This lacks granularity, real-time feedback, and verification, making it difficult for advertisers to:

*   Accurately gauge campaign reach and effectiveness.
*   Understand true audience engagement (not just potential views).
*   Optimize ad placements based on specific audience patterns.
*   Verify ad presence and quality (Proof-of-Posting).
*   Adapt campaigns based on real-time conditions (weather, events, traffic anomalies).

## Our Solution: Billboard AI

Billboard AI addresses these challenges by providing a continuous stream of rich, real-world data directly from the point of exposure. Our edge devices analyze visual and environmental data, feeding a powerful analytics and knowledge graph platform.

**Value Proposition for AEs:**

*   **Enhanced Sales:** Justify premium placements with verifiable data.
*   **Client Retention:** Provide transparent, detailed performance reports.
*   **Campaign Optimization:** Advise clients on best locations, times, and creatives based on real data.
*   **Operational Efficiency:** Automate Proof-of-Posting and quality checks.

## Key Features

### 1. Real-Time Audience Analytics (Computer Vision Models)

Our core module leverages multiple CV models running on edge devices attached to billboard structures.

*   **Traffic Analysis (Vehicle & Pedestrian):**
    *   **Counting:** Accurate counts of vehicles and pedestrians passing the billboard.
    *   **Classification:** Differentiating between vehicle types (cars, trucks, buses, motorcycles) and pedestrians.
    *   **Flow & Speed:** Analyzing traffic speed, congestion patterns, and pedestrian flow direction.
    *   *(Potential Enhancement):* **Demographic Inference (Vehicle-Based):** Analyzing vehicle make/model/age distribution (where feasible and privacy-compliant) combined with time-of-day data to *infer* potential audience demographics (e.g., luxury vehicles during commute times vs. commercial vans mid-day). *This requires careful validation and privacy considerations.*

*   **Attention Metrics (Gaze/Head Pose Estimation):**
    *   **Opportunity-to-See (OTS) Refinement:** Detects faces oriented *towards* the billboard, providing a more accurate measure of potential viewers compared to simple traffic counts.
    *   **Estimated Engagement Duration:** Measures the approximate time individuals (pedestrians or vehicle occupants, where visible) are oriented towards the ad space. *Note: Precise eye-tracking (gaze) from distance is challenging; this focuses on head pose as a proxy for attention.*

*   **Anonymized Vehicle Identification & Frequency:**
    *   Track the frequency of unique vehicles passing specific locations over time (e.g., is it the same commuter traffic daily, or constantly new vehicles?). This helps understand audience churn and reach frequency *without storing personally identifiable information (PII)*. *Strict anonymization techniques (e.g., hashing with salting, feature extraction) are essential here.*

*   **Contextual Analysis:**
    *   **Weather Correlation:** Automatically logs weather conditions (sunny, rainy, cloudy, snowy) and correlates them with traffic patterns and ad visibility/effectiveness.
    *   **Temporal Trends:** Identifies daily, weekly, and seasonal patterns in traffic and audience attention specific to each billboard location.

### 2. Automated Proof-of-Posting (PoP) & Quality Control

*   **VLM-Powered Verification:** Utilizes Vision Language Models (or simpler image differencing/feature matching) to:
    *   Confirm the correct vinyl/creative is displayed.
    *   Detect damage (tears, fading), obstructions, or improper installation.
    *   Generate automated alerts for the operations team, ensuring brand safety and campaign integrity.

### 3. Market Intelligence Knowledge Graph

*   **Holistic Market View:** Creates a dynamic, visual representation of all billboard assets within a market.
*   **Relationship Mapping:** Connects structures based on:
    *   **Geospatial Data:** Location, proximity to points of interest (malls, highways, event venues), competitor locations.
    *   **Traffic Data:** Real-time and historical traffic flow from our sensors and potentially external APIs.
    *   **Client Data:** Advertiser locations, target audience zones, campaign history.
    *   **Campaign Performance:** Linking actual impression and engagement data back to specific campaigns and structures.
*   **Optimization Engine:** Uses the knowledge graph to identify:
    *   High-performing / under-utilized structures.
    *   Optimal structure combinations for specific campaign goals and target audiences.
    *   Synergies between client locations and billboard placements.
*   **Technology:** Leverages the **Palantir AIP Ontology SDK** (or similar graph database technologies like Neo4j, Neptune) to model and query these complex relationships effectively.

## Technology Stack

*   **Edge Hardware:**
    *   **Compute:** Testing platforms like Raspberry Pi 5 (potentially with AI HAT+ for acceleration) and specialized SoCs like the one in the OpenMV N6. Evaluating performance, power consumption, thermal management, and cost for a custom solution.
    *   **Sensors:**
        *   **Cameras:** Utilizing Raspberry Pi Global Shutter (for fast-moving vehicles) and NoIR cameras (for low-light/night performance). Exploring optimal lens types, resolutions, and frame rates.
        *   *(Potential Addition):* Environmental sensors (temperature, humidity, ambient light).
    *   **Connectivity:** Cellular (LTE/5G), Wi-Fi (for setup/maintenance), potentially LoRaWAN for basic telemetry/status if cellular is unavailable/costly.
    *   **Enclosure:** Weatherproof (IP65+), tamper-resistant housing with appropriate mounting.
*   **Edge Software:**
    *   **OS:** Linux (e.g., Raspberry Pi OS, Yocto for custom builds).
    *   **CV Libraries:** OpenCV, PyTorch Mobile / TensorFlow Lite for on-device model inference.
    *   **AI Models:** Custom trained models for object detection (YOLO variants, SSD), face detection, head pose estimation, potentially feature extraction for anonymized vehicle ID. VLM for PoP.
    *   **Orchestration:** Containerization (Docker/Balena) for deployment and updates. Secure communication protocols (MQTT over TLS, HTTPS).
*   **Cloud Backend:**
    *   **Data Ingestion:** Message Queues (e.g., Kafka, RabbitMQ, AWS Kinesis, Google Pub/Sub).
    *   **Storage:** Time-series databases (e.g., InfluxDB, TimescaleDB) for sensor data, Relational/NoSQL databases for metadata, Blob storage for images/video snippets (if needed for PoP verification).
    *   **Processing:** Cloud functions / containerized services for aggregation, analysis, reporting, KG updates.
    *   **Knowledge Graph:** Palantir AIP / Neo4j / AWS Neptune / Azure Cosmos DB (Graph API).
    *   **API:** RESTful or GraphQL API for data access.
*   **Frontend / Dashboard:**
    *   Web application (React, Vue, Angular) for AEs and advertisers to view dashboards, reports, alerts, and KG visualizations.
    *   Mapping libraries (Mapbox, Leaflet) for geospatial visualization.

**Flow:**
1.  **Capture:** Cameras and sensors on the edge device collect raw data.
2.  **Edge Process:** CV models process data locally to extract key information (counts, types, attention flags, anonymized IDs, PoP status). This minimizes data transmission needs.
3.  **Transmit:** Aggregated, anonymized data and PoP alerts are sent securely to the cloud backend.
4.  **Cloud Process & Store:** Data is ingested, cleaned, stored, and further analyzed. Correlations are made (e.g., weather impact).
5.  **Update Knowledge Graph:** Insights and relationships are updated in the KG.
6.  **Serve Data:** Processed data and KG insights are made available via API to the frontend dashboard.

## Data Privacy and Ethics Considerations

*   **Anonymization by Design:** Processing occurs primarily on the edge. Only aggregated counts, anonymized identifiers (designed to be non-reversible to PII), and event flags (e.g., face detected facing billboard) are typically sent to the cloud.
*   **No Facial Recognition:** We detect faces for orientation (head pose) but do not perform facial *recognition* or store facial images unless explicitly required and consented to for specific PoP audit trails (and even then, with strict controls).
*   **License Plate Handling:** We are **avoiding direct license plate capture and storage** due to significant privacy implications and legal restrictions (like GDPR, CCPA). Focus is on anonymized vehicle frequency analysis. Any approach involving vehicle characteristics must be carefully vetted against local regulations.
*   **Data Minimization:** We only collect and process data essential for the defined analytics.
*   **Security:** End-to-end encryption for data transmission, secure storage, access controls.
*   **Transparency:** Clear documentation on what data is collected, how it's processed, and how privacy is maintained.

## Current Status & Roadmap

*   **[Current Stage]:** Currently testing COTS hardware (OpenMV N6, RPi 5 + AI HAT/Cameras) and developing initial CV models. Building proof-of-concept for core features. Setting up initial Knowledge Graph schema with Palantir AIP SDK.
*   **[Next Steps]:**
    *   Refine CV model accuracy and efficiency for edge deployment.
    *   Develop robust data anonymization techniques.
    *   Build out cloud infrastructure and data pipeline.
    *   Design and prototype the AE dashboard.
    *   Begin design of custom hardware solution optimized for power, cost, and performance.
    *   Conduct pilot deployments on a small number of structures.
    *   Perform legal and privacy reviews for target markets.

## Deployment Considerations

*   **Power:** Requires reliable power source at the billboard structure (potentially solar + battery if grid power is unavailable).
*   **Connectivity:** Stable internet connection (Cellular likely most common).
*   **Installation:** Secure, weatherproof mounting that provides optimal camera views without obstructing the advertisement.
*   **Maintenance:** Remote monitoring, over-the-air updates, potential for physical servicing.
*   **Calibration:** Initial camera calibration per site may be required.

## Hardware Components Under Evaluation

*   **Microcontroller/SoC:**
    *   OpenMV N6: [https://openmv.io/collections/all-products/products/openmv-n6?variant=41573456576606](https://openmv.io/collections/all-products/products/openmv-n6?variant=41573456576606)
    *   Raspberry Pi 5 (16GB): [https://www.raspberrypi.com/products/raspberry-pi-5/](https://www.raspberrypi.com/products/raspberry-pi-5/)
*   **AI Acceleration:**
    *   Raspberry Pi AI HAT+: [https://www.raspberrypi.com/products/ai-hat/](https://www.raspberrypi.com/products/ai-hat/)
*   **Cameras:**
    *   Raspberry Pi Global Shutter Camera: [https://www.raspberrypi.com/products/raspberry-pi-global-shutter-camera/](https://www.raspberrypi.com/products/raspberry-pi-global-shutter-camera/)
    *   Raspberry Pi Camera Module 2 NoIR: [https://www.raspberrypi.com/products/pi-noir-camera-v2/](https://www.raspberrypi.com/products/pi-noir-camera-v2/)

*(Note: These are COTS options for prototyping; a custom hardware solution is planned for scaled deployment.)*

## Contributing / Contact

*[Optional: Add information on how others can contribute or get in touch, e.g., Link to contribution guidelines, contact email]*
