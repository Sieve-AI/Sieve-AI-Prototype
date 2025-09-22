# Sieve-AI-Prototype: BigQuery AI Data Intelligence System

This repository contains the source code for a prototype that transforms and analyzes unstructured and semi-structured data. It leverages `Google Cloud`'s `BigQuery AI` and `Gemini` models to process diverse files and generate actionable insights.

## ⚙️ Technical Overview

The system is a *Multimodal Pioneer* that implements a "*structural redistribution*" methodology to solve the "*bias of interpretation*" in raw data. The core process is a three-phase workflow:

**Data Classification:** Ingests and standardizes various file types (*text, images, audio*) into `JSON` format.

**Data Processing:** Uses `BigQuery AI` and `Gemini` to perform deep analysis, pattern recognition, and make "*smart predictions.*"

**Deliverable Preparation:** Transforms processed data into final outputs.

## 🛠️ Key Technologies

**BigQuery:** The central platform for data warehousing and AI functions.

**Pandas:** Used for manipulating structured datasets in `Python`.

**Gemini:** The AI model for interpreting unstructured data.

**Cloud Storage:** For initial file ingestion.

**JSON & CSV:** For data standardization and final output.

**Docker:** For consistent and reproducible environments.

## 🔬 Implementation & Logic

The system classifies data into four core classes:

**Measure:** For quantitative data.

**Label:** For descriptive and categorical data.

**Transact:** For event-based and time-series data.

**Condition:** For states, ratings, and logical values.

Data is transformed following a logical "*control route*" based on predefined compatibility rules. For example, to get a prediction report, the system processes *Measure and Transact* data.

## 📊 Architecture

The architecture is a three-stage pipeline:

**Ingestion:** 
Raw files → Cloud Storage → File Validation → `JSON` format.

**Processing:** 
JSON data → Middleware → Specialized Processors (*audio_processor.py, image_processor.py*) → AI Models (*BigQuery AI, Gemini*) for analysis.

**Delivery:** 
Processed data → Reports (*with risk analysis*), a Dashboard, and a unified `.csv` Dataset.

## 📁 Repository Structure

```
├── README.md├── .gitignore
├── cloudbuild.yaml
├── config.py
├── Dockerfile
├── main.py
├── requirements.txt
└── /utils
    ├── _init_.py
    ├── audio_processor.py
    ├── bigframes_processor.py
    ├── data_processor.py
    ├── dataframe_processor.py
    ├── file_mover.py
    ├── file_validator.py
    ├── image_processor.py
    ├── magic_checker.py
    ├── schema.py
    └── test_audio.py
```

## 📹 Video Demo

Video: https://youtu.be/KuITitAtRBQ?si=dwNXLLUhuwPxwL7

## ⚠️ Important Note

This is the completed prototype, uploaded without previous version histories. Our team, based in Venezuela, had to work locally due to significant challenges from power outages and unreliable internet connections, a reality of our socio-political context. Despite these difficulties, we are proud to deliver a working version of the prototype.
