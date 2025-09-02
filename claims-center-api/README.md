# GW Claims Center API Client

A lightweight Python framework for interacting with Guidewire Claims Center API.

## Structure
- `src/`: Core client and query functions
- `docs/`: Business use cases and project rationale
- `notebooks/`: Interactive test queries
- `tests/`: Unit tests
- `.env.example`: Environment variables

## Quick start
```bash
pip install -r requirements.txt

## Claims Queries Module

This module provides a set of reusable queries to interact with Guidewire ClaimCenter API.  
It is designed to support claim data retrieval and validation scenarios, enabling flexible testing and integration.  

### Components
- **api_client.py** → Handles API request/response cycle with proper error handling.  
- **claims_queries.py** → Contains sample queries for claims retrieval and related operations.  

### Usage
Import the module in your Python project and configure the required environment variables for authentication.  
Queries can be executed directly through  or integrated into higher-level workflows.  

