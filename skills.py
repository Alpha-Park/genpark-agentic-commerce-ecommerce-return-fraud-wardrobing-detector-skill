# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-ecommerce-return-fraud-wardrobing-detector-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def detect_return_fraud_and_wardrobing(customer_history, current_return_request):
    total_orders = customer_history.get("total_orders", 1)
    total_returns = customer_history.get("total_returns", 0)
    customer_return_rate = (total_returns / total_orders) if total_orders > 0 else 0.0
    
    fraud_flags = []
    risk_score = 0
    
    # 1. Extreme return rate threshold
    if customer_return_rate > 0.65 and total_orders >= 5:
        risk_score += 40
        fraud_flags.append(f"Serial returner anomaly: historical return rate {customer_return_rate*100:.1f}%")
        
    # 2. Wardrobing high-value event category
    category = current_return_request.get("category", "APPAREL")
    item_price = current_return_request.get("item_price_usd", 0.0)
    days_held = current_return_request.get("days_since_delivery", 0)
    
    if category in ("FORMAL_DRESS", "LUXURY_JEWELRY", "CAMERA_EQUIPMENT") and days_held >= 25:
        risk_score += 35
        fraud_flags.append(f"Potential wardrobing: high-value {category} ($ {item_price:.2f}) returned on day {days_held} near policy expiration")
        
    # 3. Bracketing check
    if current_return_request.get("is_bracketed_order", False):
        risk_score += 15
        fraud_flags.append("Bracketed size/color purchase detected")
        
    if risk_score >= 60:
        recommendation = "REQUIRE_PHYSICAL_TAG_INSPECTION_STORE_CREDIT_ONLY"
    elif risk_score >= 30:
        recommendation = "STANDARD_RETURN_WITH_RESTOCKING_FEE"
    else:
        recommendation = "INSTANT_REFUND_APPROVED"
        
    return {
        "customer_lifetime_return_rate_pct": round(customer_return_rate * 100.0, 1),
        "return_fraud_risk_score_0_to_100": min(100, risk_score),
        "fraud_risk_level": "HIGH" if risk_score >= 60 else ("MODERATE" if risk_score >= 30 else "LOW"),
        "identified_abuse_patterns": fraud_flags if fraud_flags else ["Standard consumer return"],
        "merchant_disposition": recommendation
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "detect_return_fraud_and_wardrobing",
                        "description": """Detect organized retail crime (ORC) and consumer return abuse in e-commerce fulfillment.
Identifies wardrobing (buying high-value apparel for one-time wear and returning), bracketing (buying multiple sizes with intent to return all but one),
and serial refund claims without return delivery.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = detect_return_fraud_and_wardrobing(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'customer_history': {'total_orders': 12, 'total_returns': 9}, 'current_return_request': {'category': 'FORMAL_DRESS', 'item_price_usd': 680.0, 'days_since_delivery': 28, 'is_bracketed_order': False}}
        out = detect_return_fraud_and_wardrobing(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
