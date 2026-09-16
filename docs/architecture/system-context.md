# Atlas System Context

## Purpose

Atlas is a local-first portfolio research and risk-learning application. It
combines user-provided sample portfolio data with public financial information
to produce evidence-backed research insights.

Atlas is an educational engineering project. It is not investment advice, a
trading platform, or a real-time market-data system.

## System context

```text
                         ┌─────────────────────────┐
                         │          User           │
                         │ Learner / Research user │
                         └────────────┬────────────┘
                                      │
                         Imports portfolio data
                         Asks research questions
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                              Atlas                               │
│                                                                  │
│  - Validates portfolio data                                      │
│  - Stores source metadata and evidence                           │
│  - Calculates deterministic financial metrics                    │
│  - Retrieves relevant filing content                             │
│  - Produces cited research summaries                             │
│                                                                  │
└───────────────┬───────────────────────┬──────────────────────────┘
                │                       │
                │ retrieves             │ generates summaries
                ▼                       ▼
┌────────────────────────┐     ┌────────────────────────┐
│ Public data providers  │     │ Model providers        │
│                        │     │                        │
│ - SEC EDGAR filings    │     │ - Embedding model      │
│ - FRED economic data   │     │ - Language model       │
│ - Future market data   │     │                        │
└────────────────────────┘     └────────────────────────┘
```

## Responsibilities

### Atlas owns

- Validation of portfolio input
- Storage of portfolio, source, and evidence metadata
- Deterministic calculations
- Retrieval and citation construction
- Authentication and authorization when introduced
- Logging, evaluation, and operational monitoring
- Safe boundaries around model and tool usage

### Users own

- The portfolio data they choose to import
- Their interpretation and use of research output
- Verifying information before making financial decisions

### External providers own

- Availability and correctness of their data or model services
- Their API contracts, rate limits, licensing, and terms of use
- Changes to their schemas or service behavior

## Trust boundaries

Atlas must treat external data and model output as untrusted input.

Examples of risks that will be addressed as the project evolves include:

- Incorrect, missing, delayed, or restated financial data
- Malicious instructions embedded in external documents
- Model hallucinations or unsupported conclusions
- Provider outages and rate limits
- Unauthorized access to a user's portfolio data

## Current scope

This document describes the intended system boundary. Atlas does not yet
integrate with external providers, persist data, generate model output, or
expose an API.