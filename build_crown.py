#!/usr/bin/env python3
"""
FreeTheWeb — CROWN Demo Build
Builds the CROWN luxury brand site using the enhanced engine.
"""
import sys
sys.path.insert(0, '/root/freetheweb')

from engine import SiteBuilder

crown_config = {
    "business_name": "CROWN",
    "tagline": "Redefine Luxury",
    "tagline_badge": "Spring / Summer 2026",
    "hero_headline": 'Redefine<br><span style="color: {{PRIMARY_COLOR}}; font-style: italic">Luxury</span>',
    "hero_subtext": "Crafted for those who refuse to blend in. Each piece, a statement of defiance.",
    "hero_image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1600&q=80",
    "primary_color": "#c9a96e",
    "secondary_color": "#050505",
    "meta_description": "CROWN — Redefining luxury for those who refuse to blend in. Handcrafted, premium, timeless.",
    
    "products": [
        {
            "name": "The Sovereign",
            "description": "Italian leather. Hand-stitched. Uncompromising.",
            "price_cents": 24900,
            "currency": "usd",
            "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80",
            "badge": '<span class="absolute top-4 left-4 px-3 py-1 text-brand-dark text-[10px] font-medium tracking-widest uppercase" style="background: {{PRIMARY_COLOR}}">Limited</span>',
            "stripe_link": "https://buy.stripe.com/test_4gM3cxehp9XtfdW8ti57W0N",
        },
        {
            "name": "The Eclipse",
            "description": "Midnight cashmere. Draped in silence.",
            "price_cents": 18900,
            "currency": "usd",
            "image_url": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=600&q=80",
            "badge": "",
            "stripe_link": "https://buy.stripe.com/test_bJe14pfltd9F2raeRG57W0O",
        },
        {
            "name": "The Meridian",
            "description": "Structured silhouette. Everyday defiance.",
            "price_cents": 12900,
            "currency": "usd",
            "image_url": "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=600&q=80",
            "badge": '<span class="absolute top-4 left-4 px-3 py-1 bg-white/10 backdrop-blur text-white text-[10px] font-medium tracking-widest uppercase">New Season</span>',
            "stripe_link": "https://buy.stripe.com/test_9B6fZjgpx4D94zieRG57W0P",
        },
    ],
    
    "products_subtext": "Three defining pieces. Each one an extension of your identity.",
    
    "features": [
        {"title": "Source", "description": "Materials hand-selected from Italian tanneries, Japanese mills, and Scottish woolens. No shortcuts. No substitutions.", "icon": "I"},
        {"title": "Craft", "description": "Each piece passes through 14 stages of hand-finishing. Our artisans average 22 years of experience.", "icon": "II"},
        {"title": "Deliver", "description": "Presented in hand-made packaging. Delivered with white-glove care. Every detail considered.", "icon": "III"},
    ],
    "features_subtext": "How We Create",
    
    "cta_headline": 'Be <span style="font-style: italic; color: {{PRIMARY_COLOR}}">First</span>',
    "cta_subtext": "Exclusive access to new collections, private events, and pieces before they go public.",
    "cta_button": "Join",
    
    "footer_description": "Redefining luxury for those who refuse to blend in.",
    
    # Chatwoot integration (optional)
    "chatwoot_token": "",  # Add token to enable live chat
    "chatwoot_url": "https://app.chatwoot.com",
}

if __name__ == "__main__":
    builder = SiteBuilder(crown_config)
    path = builder.save("crown")
    print(f"\n🔗 Open: file://{path}")
    print("Then deploy with: wrangler pages deploy output/crown --project-name freetheweb")
