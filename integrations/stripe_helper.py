#!/usr/bin/env python3
"""
FreeTheWeb — Stripe Integration Helper
Creates products, prices, payment links, and subscription plans via Stripe MCP.
Used by the agent orchestration layer.

This script documents the exact MCP calls the agent makes.
The agent calls these functions directly, not via subprocess.
"""

# === PRODUCT CATALOG STRUCTURE ===
# The agent builds this from user's natural language request

EXAMPLE_CATALOG = {
    "business_name": "CROWN",
    "products": [
        {
            "name": "The Sovereign",
            "description": "Italian leather. Hand-stitched. Uncompromising.",
            "price_cents": 24900,
            "currency": "usd",
            "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80",
            "badge": "Limited",
            "type": "one_time",  # or "recurring"
        },
        {
            "name": "The Eclipse",
            "description": "Midnight cashmere. Draped in silence.",
            "price_cents": 18900,
            "currency": "usd",
            "image_url": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=600&q=80",
            "badge": "",
            "type": "one_time",
        },
    ],
    "subscription_plans": [
        {
            "name": "CROWN Membership",
            "description": "Exclusive access to new drops, private events, and 15% off all purchases.",
            "price_cents": 2900,
            "currency": "usd",
            "interval": "month",
            "interval_count": 1,
        }
    ]
}


# === AGENT WORKFLOW ===
# Step 1: Parse user request → extract products
# Step 2: For each product:
#   a) mcp_stripe_create_product(name, description)
#   b) mcp_stripe_create_price(product_id, unit_amount, currency)
#   c) mcp_stripe_create_payment_link(price_id, quantity=1)
# Step 3: For subscriptions:
#   a) mcp_stripe_create_product(name, description)
#   b) mcp_stripe_create_price(product_id, unit_amount, currency, recurring={"interval": "month"})
#   c) mcp_stripe_create_payment_link(price_id, quantity=1)
# Step 4: Inject payment links into HTML


def format_price(cents: int) -> str:
    """Convert cents to display format: 24900 → $249.00"""
    return f"${cents / 100:,.2f}"


def generate_stripe_calls(catalog: dict) -> list:
    """Generate the sequence of MCP calls the agent should make."""
    calls = []
    
    for product in catalog.get("products", []):
        calls.append({
            "tool": "mcp_stripe_create_product",
            "args": {
                "name": product["name"],
                "description": product["description"],
            }
        })
        calls.append({
            "tool": "mcp_stripe_create_price",
            "args": {
                "product": "{{PRODUCT_ID}}",  # filled by agent after create_product
                "unit_amount": product["price_cents"],
                "currency": product["currency"],
            }
        })
        calls.append({
            "tool": "mcp_stripe_create_payment_link",
            "args": {
                "price": "{{PRICE_ID}}",  # filled by agent after create_price
                "quantity": 1,
            }
        })
    
    for plan in catalog.get("subscription_plans", []):
        calls.append({
            "tool": "mcp_stripe_create_product",
            "args": {
                "name": plan["name"],
                "description": plan["description"],
            }
        })
        calls.append({
            "tool": "mcp_stripe_create_price",
            "args": {
                "product": "{{PRODUCT_ID}}",
                "unit_amount": plan["price_cents"],
                "currency": plan["currency"],
                "recurring": {
                    "interval": plan["interval"],
                    "interval_count": plan["interval_count"],
                }
            }
        })
        calls.append({
            "tool": "mcp_stripe_create_payment_link",
            "args": {
                "price": "{{PRICE_ID}}",
                "quantity": 1,
            }
        })
    
    return calls


if __name__ == "__main__":
    calls = generate_stripe_calls(EXAMPLE_CATALOG)
    print(f"Generated {len(calls)} Stripe MCP calls:")
    for i, call in enumerate(calls, 1):
        print(f"  {i}. {call['tool']}({json.dumps(call['args'], indent=4)})")
