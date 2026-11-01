# genpark-agentic-commerce-ecommerce-return-fraud-wardrobing-detector-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Omnichannel return fraud detection: wardrobing, receipt reuse, bracket ordering & return merchant chargeback preventer.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `detect_return_fraud_and_wardrobing`
- **Category**: `agentic_commerce`

### Method Documentation
Detect organized retail crime (ORC) and consumer return abuse in e-commerce fulfillment.
Identifies wardrobing (buying high-value apparel for one-time wear and returning), bracketing (buying multiple sizes with intent to return all but one),
and serial refund claims without return delivery.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "detect_return_fraud_and_wardrobing",
    "arguments": {
    "customer_history": {
        "total_orders": 12,
        "total_returns": 9
    },
    "current_return_request": {
        "category": "FORMAL_DRESS",
        "item_price_usd": 680.0,
        "days_since_delivery": 28,
        "is_bracketed_order": false
    }
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
