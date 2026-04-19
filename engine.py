#!/usr/bin/env python3
"""
FreeTheWeb — Assembly Engine v2
Multi-template, multi-integration website builder.

Supports:
- Multiple template styles (luxury, minimal, agency, ecommerce)
- Stripe products + subscriptions + payment links
- Chatwoot live chat widget
- Cloudflare Pages deployment
- GitHub repo creation
"""
import os
import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
COMPONENTS_DIR = BASE_DIR / "components"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


class SiteBuilder:
    def __init__(self, config: dict):
        self.config = config
        self.html = ""
    
    def build(self) -> str:
        """Build complete site HTML from config."""
        style = self.config.get("style", "luxury")
        self.html = self._load_template(style)
        
        # Core replacements
        self._replace({
            "{{BUSINESS_NAME}}": self.config["business_name"],
            "{{TAGLINE}}": self.config.get("tagline", "Premium Quality"),
            "{{META_DESCRIPTION}}": self.config.get("meta_description", ""),
            "{{PRIMARY_COLOR}}": self.config.get("primary_color", "#c9a96e"),
            "{{SECONDARY_COLOR}}": self.config.get("secondary_color", "#050505"),
            "{{YEAR}}": str(datetime.now().year),
        })
        
        # Inject components
        self._inject_navbar()
        self._inject_hero()
        self._inject_products()
        self._inject_features()
        self._inject_cta()
        self._inject_footer()
        
        # Inject integrations
        if self.config.get("chatwoot_token"):
            self._inject_chatwoot()
        
        # Inject Stripe checkout script
        self._inject_stripe()
        
        return self.html
    
    def _load_template(self, style: str) -> str:
        """Load template by style name."""
        template_path = TEMPLATES_DIR / f"{style}.html"
        if not template_path.exists():
            template_path = TEMPLATES_DIR / "luxury.html"
        with open(template_path) as f:
            return f.read()
    
    def _replace(self, replacements: dict):
        for placeholder, value in replacements.items():
            self.html = self.html.replace(placeholder, str(value))
    
    def _inject_navbar(self):
        nav = self._load_component("navbar")
        nav = nav.replace("{{BUSINESS_NAME}}", self.config["business_name"])
        nav = nav.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        self.html = self.html.replace("{{NAVBAR}}", nav)
    
    def _inject_hero(self):
        hero = self._load_component("hero")
        hero = hero.replace("{{BUSINESS_NAME}}", self.config["business_name"])
        hero = hero.replace("{{TAGLINE_BADGE}}", self.config.get("tagline_badge", ""))
        hero = hero.replace("{{HERO_HEADLINE}}", self.config.get("hero_headline", ""))
        hero = hero.replace("{{HERO_SUBTEXT}}", self.config.get("hero_subtext", ""))
        hero = hero.replace("{{HERO_IMAGE}}", self.config.get("hero_image", ""))
        hero = hero.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        self.html = self.html.replace("{{HERO}}", hero)
    
    def _inject_products(self):
        section = self._load_component("products")
        cards = ""
        for p in self.config.get("products", []):
            cards += self._build_product_card(p)
        section = section.replace("{{PRODUCT_CARDS}}", cards)
        section = section.replace("{{PRODUCTS_SUBTEXT}}", self.config.get("products_subtext", ""))
        section = section.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        self.html = self.html.replace("{{PRODUCTS}}", section)
    
    def _build_product_card(self, product: dict) -> str:
        card = self._load_component("product-card")
        badge_html = product.get("badge", "")
        
        card = card.replace("{{PRODUCT_NAME}}", product["name"])
        card = card.replace("{{PRODUCT_DESCRIPTION}}", product.get("description", ""))
        card = card.replace("{{PRODUCT_PRICE}}", self._format_price(product.get("price_cents", 0)))
        card = card.replace("{{PRODUCT_IMAGE}}", product.get("image_url", ""))
        card = card.replace("{{STRIPE_PAYMENT_LINK}}", product.get("stripe_link", "#"))
        card = card.replace("{{BADGE}}", badge_html)
        card = card.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        return card
    
    def _inject_features(self):
        section = self._load_component("features")
        cards = ""
        for f in self.config.get("features", []):
            cards += self._build_feature_card(f)
        section = section.replace("{{FEATURE_CARDS}}", cards)
        section = section.replace("{{FEATURES_SUBTEXT}}", self.config.get("features_subtext", ""))
        section = section.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        self.html = self.html.replace("{{FEATURES}}", section)
    
    def _build_feature_card(self, feature: dict) -> str:
        card = self._load_component("feature-card")
        card = card.replace("{{FEATURE_TITLE}}", feature["title"])
        card = card.replace("{{FEATURE_DESCRIPTION}}", feature["description"])
        card = card.replace("{{FEATURE_ICON}}", feature.get("icon", "✦"))
        card = card.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        return card
    
    def _inject_cta(self):
        cta = self._load_component("cta")
        cta = cta.replace("{{CTA_HEADLINE}}", self.config.get("cta_headline", ""))
        cta = cta.replace("{{CTA_SUBTEXT}}", self.config.get("cta_subtext", ""))
        cta = cta.replace("{{CTA_BUTTON_TEXT}}", self.config.get("cta_button", "Shop Now"))
        cta = cta.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        self.html = self.html.replace("{{CTA}}", cta)
    
    def _inject_footer(self):
        footer = self._load_component("footer")
        footer = footer.replace("{{BUSINESS_NAME}}", self.config["business_name"])
        footer = footer.replace("{{YEAR}}", str(datetime.now().year))
        footer = footer.replace("{{FOOTER_DESCRIPTION}}", self.config.get("footer_description", ""))
        footer = footer.replace("{{PRIMARY_COLOR}}", self.config.get("primary_color", "#c9a96e"))
        self.html = self.html.replace("{{FOOTER}}", footer)
    
    def _inject_chatwoot(self):
        """Inject Chatwoot live chat widget."""
        token = self.config["chatwoot_token"]
        base_url = self.config.get("chatwoot_url", "https://app.chatwoot.com")
        
        chatwoot_script = f"""
<!-- Chatwoot Live Chat -->
<script>
  (function(d,t) {{
    var BASE_URL="{base_url}";
    var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
    g.src=BASE_URL+"/packs/js/sdk.js";
    g.defer=!0;g.async=!0;s.parentNode.insertBefore(g,s);
    g.onload=function(){{
      window.chatwootSDK.run({{
        websiteToken: '{token}',
        baseUrl: BASE_URL
      }})
    }}
  }})(document,"script");
</script>
"""
        self.html = self.html.replace("</body>", chatwoot_script + "\n</body>")
    
    def _inject_stripe(self):
        """Inject Stripe.js for checkout."""
        stripe_script = '<script src="https://js.stripe.com/v3/"></script>'
        self.html = self.html.replace("</head>", stripe_script + "\n</head>")
    
    def _load_component(self, name: str) -> str:
        path = COMPONENTS_DIR / f"{name}.html"
        if path.exists():
            with open(path) as f:
                return f.read()
        return ""
    
    def _format_price(self, cents: int) -> str:
        return f"${cents / 100:,.2f}"
    
    def save(self, output_name: str = None) -> str:
        """Build and save to output directory."""
        html = self.build()
        name = output_name or self.config["business_name"].lower().replace(" ", "-")
        output_path = OUTPUT_DIR / name
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / "index.html"
        with open(filepath, "w") as f:
            f.write(html)
        
        # Save config
        with open(output_path / "config.json", "w") as f:
            json.dump(self.config, f, indent=2)
        
        print(f"✅ Site built: {filepath}")
        return str(filepath)


# === CONVENIENCE ===
def build_site(config: dict, name: str = None) -> str:
    builder = SiteBuilder(config)
    return builder.save(name)
