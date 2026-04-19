#!/usr/bin/env python3
"""
FreeTheWeb Assembly Engine
Takes user request + brand info → outputs complete website HTML
"""
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPONENTS_DIR = os.path.join(BASE_DIR, "components")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def load_component(name: str) -> str:
    path = os.path.join(COMPONENTS_DIR, f"{name}.html")
    with open(path) as f:
        return f.read()


def load_template() -> str:
    path = os.path.join(TEMPLATES_DIR, "base.html")
    with open(path) as f:
        return f.read()


def build_product_card(name: str, description: str, price: str, 
                        image: str, stripe_link: str, badge: str = "") -> str:
    card = load_component("product-card")
    badge_html = f'<span class="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-semibold text-white" style="background: var(--primary)">{badge}</span>' if badge else ""
    card = card.replace("{{PRODUCT_NAME}}", name)
    card = card.replace("{{PRODUCT_DESCRIPTION}}", description)
    card = card.replace("{{PRODUCT_PRICE}}", price)
    card = card.replace("{{PRODUCT_IMAGE}}", image)
    card = card.replace("{{STRIPE_PAYMENT_LINK}}", stripe_link)
    card = card.replace("{{BADGE}}", badge_html)
    return card


def build_feature_card(title: str, description: str, icon: str = "✦") -> str:
    card = load_component("feature-card")
    card = card.replace("{{FEATURE_TITLE}}", title)
    card = card.replace("{{FEATURE_DESCRIPTION}}", description)
    card = card.replace("{{FEATURE_ICON}}", icon)
    return card


def assemble_site(config: dict) -> str:
    """Assemble a complete site from config dict."""
    html = load_template()
    
    # Basic replacements
    replacements = {
        "{{BUSINESS_NAME}}": config["business_name"],
        "{{TAGLINE}}": config.get("tagline", "Premium Quality"),
        "{{META_DESCRIPTION}}": config.get("meta_description", f"{config['business_name']} — {config.get('tagline', 'Shop now')}"),
        "{{PRIMARY_COLOR}}": config.get("primary_color", "#000000"),
        "{{SECONDARY_COLOR}}": config.get("secondary_color", "#333333"),
        "{{YEAR}}": str(datetime.now().year),
    }
    
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)
    
    # Load and inject components
    navbar = load_component("navbar")
    navbar = navbar.replace("{{BUSINESS_NAME}}", config["business_name"])
    navbar = navbar.replace("{{LOGO}}", _build_logo(config))
    html = html.replace("{{NAVBAR}}", navbar)
    
    hero = load_component("hero")
    hero = hero.replace("{{BUSINESS_NAME}}", config["business_name"])
    hero = hero.replace("{{TAGLINE_BADGE}}", config.get("tagline_badge", "New Collection"))
    hero = hero.replace("{{HERO_HEADLINE}}", config.get("hero_headline", f"Welcome to {config['business_name']}"))
    hero = hero.replace("{{HERO_SUBTEXT}}", config.get("hero_subtext", config.get("tagline", "Premium products for everyone")))
    hero = hero.replace("{{HERO_IMAGE}}", config.get("hero_image", "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&q=80"))
    html = html.replace("{{HERO}}", hero)
    
    # Products section
    products_section = load_component("products")
    product_cards = ""
    for p in config.get("products", []):
        product_cards += build_product_card(
            name=p["name"],
            description=p.get("description", ""),
            price=p["price"],
            image=p.get("image", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&q=80"),
            stripe_link=p.get("stripe_link", "#"),
            badge=p.get("badge", "")
        ) + "\n"
    products_section = products_section.replace("{{PRODUCT_CARDS}}", product_cards)
    products_section = products_section.replace("{{PRODUCTS_SUBTEXT}}", config.get("products_subtext", "Handpicked for you"))
    html = html.replace("{{PRODUCTS}}", products_section)
    
    # Features section
    features_section = load_component("features")
    feature_cards = ""
    for f in config.get("features", [
        {"title": "Premium Quality", "description": "Every product is carefully selected and quality-tested.", "icon": "✦"},
        {"title": "Fast Shipping", "description": "Free shipping on orders over $50. Arrives in 3-5 days.", "icon": "⚡"},
        {"title": "Easy Returns", "description": "30-day return policy. No questions asked.", "icon": "↩"},
    ]):
        feature_cards += build_feature_card(
            title=f["title"],
            description=f["description"],
            icon=f.get("icon", "✦")
        ) + "\n"
    features_section = features_section.replace("{{FEATURE_CARDS}}", feature_cards)
    features_section = features_section.replace("{{FEATURES_SUBTEXT}}", config.get("features_subtext", "What makes us different"))
    html = html.replace("{{FEATURES}}", features_section)
    
    # CTA section
    cta = load_component("cta")
    cta = cta.replace("{{CTA_HEADLINE}}", config.get("cta_headline", f"Ready to shop at {config['business_name']}?"))
    cta = cta.replace("{{CTA_SUBTEXT}}", config.get("cta_subtext", "Browse our collection and find something you love."))
    cta = cta.replace("{{CTA_BUTTON_TEXT}}", config.get("cta_button", "Shop Now"))
    html = html.replace("{{CTA}}", cta)
    
    # Footer
    footer = load_component("footer")
    footer = footer.replace("{{BUSINESS_NAME}}", config["business_name"])
    footer = footer.replace("{{LOGO}}", _build_logo(config))
    footer = footer.replace("{{FOOTER_DESCRIPTION}}", config.get("footer_description", f"{config['business_name']} — Premium products, delivered to your door."))
    footer = footer.replace("{{FOOTER_SHOP_LINKS}}", "")
    footer = footer.replace("{{FOOTER_COMPANY_LINKS}}", "")
    footer = footer.replace("{{SOCIAL_LINKS}}", "")
    footer = footer.replace("{{YEAR}}", str(datetime.now().year))
    html = html.replace("{{FOOTER}}", footer)
    
    return html


def _build_logo(config: dict) -> str:
    if config.get("logo_url"):
        return f'<img src="{config["logo_url"]}" alt="{config["business_name"]}" class="h-8 w-auto">'
    initial = config["business_name"][0].upper()
    return f'<div class="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-sm" style="background: var(--primary)">{initial}</div>'


def save_site(config: dict, output_name: str = None) -> str:
    """Build and save site to output directory."""
    html = assemble_site(config)
    name = output_name or config["business_name"].lower().replace(" ", "-")
    output_path = os.path.join(OUTPUT_DIR, name)
    os.makedirs(output_path, exist_ok=True)
    
    filepath = os.path.join(output_path, "index.html")
    with open(filepath, "w") as f:
        f.write(html)
    
    # Save config for reference
    with open(os.path.join(output_path, "config.json"), "w") as f:
        json.dump(config, f, indent=2)
    
    return filepath


# --- Example usage ---
if __name__ == "__main__":
    hat_store = {
        "business_name": "Crown Hats",
        "tagline": "Premium Headwear for Every Style",
        "tagline_badge": "New Collection 2026",
        "hero_headline": "Find Your Perfect Crown",
        "hero_subtext": "Handcrafted hats made from premium materials. Designed for those who stand out.",
        "hero_image": "https://images.unsplash.com/photo-1521369909029-2afed882baee?w=800&q=80",
        "primary_color": "#1a1a1a",
        "secondary_color": "#d4a574",
        "products": [
            {
                "name": "Classic Snapback",
                "description": "Premium cotton snapback with adjustable fit",
                "price": "$39.99",
                "image": "https://images.unsplash.com/photo-1588850561407-ed78c334e67a?w=400&q=80",
                "stripe_link": "https://buy.stripe.com/test_4gM3cxehp9XtfdW8ti57W0N",
                "badge": "Best Seller"
            },
            {
                "name": "Wool Beanie",
                "description": "Soft merino wool for cold days",
                "price": "$29.99",
                "image": "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=400&q=80",
                "stripe_link": "https://buy.stripe.com/test_bJe14pfltd9F2raeRG57W0O"
            },
            {
                "name": "Straw Fedora",
                "description": "Handwoven straw, perfect for summer",
                "price": "$59.99",
                "image": "https://images.unsplash.com/photo-1514327605112-b887c0e61c0a?w=400&q=80",
                "stripe_link": "https://buy.stripe.com/test_9B6fZjgpx4D94zieRG57W0P",
                "badge": "New"
            },
            {
                "name": "Leather Trucker",
                "description": "Vintage leather trucker cap",
                "price": "$49.99",
                "image": "https://images.unsplash.com/photo-1556306535-0f09a537f0a3?w=400&q=80",
                "stripe_link": "https://buy.stripe.com/test_5kQ8wR3CLc5Bgi0aBq57W0Q"
            }
        ],
        "features": [
            {"title": "Handcrafted Quality", "description": "Every hat is made with premium materials and attention to detail.", "icon": "✦"},
            {"title": "Free Shipping", "description": "Free shipping on all orders over $50. Arrives in 3-5 days.", "icon": "⚡"},
            {"title": "Perfect Fit Guarantee", "description": "Not happy? Return within 30 days for a full refund.", "icon": "↩"}
        ],
        "cta_headline": "Ready to Find Your Crown?",
        "cta_subtext": "Join thousands of happy customers who found their perfect hat.",
        "cta_button": "Browse Collection",
        "footer_description": "Crown Hats — Premium headwear for those who stand out. Handcrafted with love."
    }
    
    path = save_site(hat_store)
    print(f"✅ Site built: {path}")
