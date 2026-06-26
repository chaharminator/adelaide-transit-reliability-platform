# Adelaide Transit Reliability & Delay Prediction Platform

## Problem Statement

Public transport delays affect commuters, businesses, students, and transport planners. However, raw transit data is difficult to use directly because it is fragmented across schedule data, real-time vehicle updates, and trip delay feeds.

This project solves that problem by building an end-to-end data engineering platform that collects, processes, stores, and exposes Adelaide Metro transit reliability insights through APIs.

The platform helps answer questions such as:

- Which routes are most frequently delayed?
- Which stops are associated with recurring delays?
- What time periods have the highest delay risk?
- What is the expected delay for a route at a given time?

## Solution

The project builds a cloud-based ETL/ELT pipeline using Python, AWS, SQL, Docker, and FastAPI.

The system ingests Adelaide Metro GTFS and GTFS Realtime data, stores raw data in Amazon S3, transforms it into analytics-ready datasets, loads curated data into PostgreSQL/Athena, and exposes reliability metrics through FastAPI endpoints.

A small machine learning component using Amazon SageMaker will be added to predict expected delay based on route, stop, day of week, and time of day.

## Tech Stack

- Python
- SQL
- PostgreSQL
- Docker
- FastAPI
- AWS S3
- AWS Glue
- Amazon Athena
- Amazon SageMaker
- Git/GitHub

## Expected Features

- Transit data ingestion pipeline
- Raw, cleaned, and curated data layers
- Route reliability scoring
- Stop-level delay analysis
- Peak-hour delay pattern detection
- FastAPI endpoints for reliability insights
- Delay prediction model using SageMaker