# FreeTheWeb

**Build websites with natural language. Own your code. Host for free.**

An AI agent that takes your idea ("build me a hat store"), browses components, wires Stripe payments, and pushes to GitHub — so you own everything.

## How It Works

1. **Describe** your website in plain English
2. **Agent** assembles HTML from a curated component library
3. **Stripe** products and payment links are created automatically
4. **GitHub** repo is created under your account
5. **Deploy** to Cloudflare Pages (free, unlimited bandwidth)

## Demo: Crown Hats

A fully working e-commerce site built entirely by the agent.

- 4 products with real Stripe payment links
- Responsive design with Tailwind CSS
- Zero dependencies, zero build step
- [Live on Cloudflare Pages](#) ← deploy to see it live

## Project Structure

```
freetheweb/
├── components/          # HTML component library (Tailwind)
│   ├── navbar.html
│   ├── hero.html
│   ├── products.html
│   ├── product-card.html
│   ├── features.html
│   ├── feature-card.html
│   ├── cta.html
│   └── footer.html
├── templates/
│   └── base.html        # Full page template
├── assemble.py          # Assembly engine
├── output/              # Generated sites
│   └── crown-hats/      # Demo store
└── README.md
```

## Quick Start

```bash
# Clone and run the demo
git clone https://github.com/welliv/freetheweb.git
cd freetheweb
python3 assemble.py

# Output: output/crown-hats/index.html
# Open in browser to see the site
```

## The Vision

**freetheweb.net** — Every creator should own their code, host for free, and let AI handle the tedious parts.

- ❌ $74/mo Webflow plans
- ❌ Vercel commercial restrictions
- ❌ 10-20 hours of manual setup
- ✅ Agent builds it. You own it. Deploy for free.

Built for the [Hermes Agent Creative Hackathon](https://hermes.nousresearch.com) — May 2026.
