# Business Case — Red-Team-as-a-Service (RTaaS)

**Date:** April 10, 2026  
**Prepared for:** Symposium 2026 Research Engineering Track

---

## Executive Summary

RTaaS converts A-Kuo's AI safety benchmarking work into a commercial platform at the exact moment when the market is being legally compelled to buy it. The EU AI Act's August 2026 enforcement deadline is creating mandatory demand for adversarial testing services from every enterprise deploying AI in high-risk categories. RTaaS has technical differentiation (LLM-vs-LLM mutation, entropy scoring, compliance-native reports), a head start from existing benchmarking work, and a path to $10M ARR within 24 months. The window to establish a technical moat is narrow: move now, before the market consolidates.

---

## Market Context

### The Regulatory Forcing Function

**EU AI Act (effective August 2026):**
- High-risk AI systems (healthcare, legal, HR, biometrics, critical infrastructure) must undergo conformity assessment before deployment
- Article 9 requires systematic risk management including red-team style testing
- Non-compliance penalties: up to €30M or 6% of global annual turnover
- Estimated 50,000+ AI systems in scope across the EU

**NIST AI RMF (US, adopted by federal agencies and voluntary adoption accelerating):**
- MEASURE function requires documented adversarial testing
- Federal agencies subject to OMB requirements citing AI RMF compliance

**SEC Staff Bulletin on AI (US, 2025):**
- Financial firms using AI in customer-facing applications must document safety testing
- Creates pull from financial services sector specifically

The bottom line: **adversarial testing for LLMs has moved from best practice to legal requirement** in 2026. This is not a "nice to have" — it is a compliance checkbox with multi-million dollar penalty consequences.

---

## Market Size

### Total Addressable Market (TAM)
**AI Governance, Risk & Compliance (AI GRC) Market:** $3.2B in 2026, projected $18.7B by 2030 (MarketsandMarkets, 2025).  
**AI Red-Teaming / Adversarial Testing sub-segment:** ~15–20% of AI GRC, estimated $500M–$700M in 2026, growing faster than GRC overall due to regulation.

### Serviceable Addressable Market (SAM)
Enterprises deploying LLMs in regulated industries (financial, healthcare, legal, government) with >$100M annual revenue.  
Estimated ~12,000 enterprises globally. At $10K–$100K/year average contract: **SAM = $120M–$1.2B**.

### Serviceable Obtainable Market (SOM)
**Year 1:** 50–100 customers, $300K–$1.5M ARR  
**Year 2:** 200–400 customers, $2–6M ARR  
**Year 3:** 800–1500 customers (including developer tier), $10–20M ARR

---

## Competitive Landscape

| Company | Offering | Funding/Stage | Weakness vs. RTaaS |
|---------|----------|---------------|---------------------|
| **Lakera** | Prompt injection defense / Gandalf playground | $20M Series A (2024) | Defense-focused (not red-teaming); no compliance reports |
| **HiddenLayer** | ML model security, adversarial attack detection | $50M Series A (2023) | Traditional ML focus (not LLM-specific); no LLM-vs-LLM attacker |
| **Adversa AI** | AI red-team consultancy + platform | Private | Consulting-heavy, not scalable API product |
| **Garak** (NVIDIA) | Open-source LLM vulnerability scanner | Free / open-source | No compliance reports; requires ML expertise to operate; no dynamic mutation |
| **Patronus AI** | LLM evaluation / hallucination detection | $17M seed (2024) | Evaluation focus, not adversarial red-teaming; limited compliance mapping |
| **Promptfoo** | Open-source LLM testing | Open-source | Developer tool, not compliance-grade; no LLM attacker |
| **Calypso AI** | AI security platform | DARPA-backed | Government/defense focus; limited commercial LLM coverage |

**Market Gap:** No player combines (1) LLM-vs-LLM automated attack generation + (2) entropy-based scoring + (3) compliance-native reporting in a single accessible API. This is RTaaS's sweet spot.

---

## Customer Segments

### Segment 1: AI-Native Startups (Freemium → Paid)
**Who:** LLM-powered startups building in regulated spaces (AI in healthcare, legal tech, fintech)  
**Pain:** They know they need safety testing before launch; they don't have in-house red-teamers  
**Budget:** $5K–$25K/year  
**Motion:** Developer sign-up → freemium → convert on first compliance requirement  
**Volume:** High volume, lower ACV; drives platform adoption and attack library quality

### Segment 2: Enterprise AI Teams
**Who:** Data science / AI teams at Fortune 500 companies deploying LLMs in customer-facing or employee-facing applications  
**Pain:** Legal and compliance teams are asking "how do we know this is safe?" before launch  
**Budget:** $25K–$150K/year  
**Motion:** Champion in AI team → legal/compliance sponsor → procurement  
**Volume:** Medium volume, higher ACV; core revenue engine

### Segment 3: Compliance & Legal Departments (New Buyer)
**Who:** Chief Compliance Officers, GCs, legal teams at banks, insurance companies, healthcare systems  
**Pain:** EU AI Act compliance deadline; need to demonstrate due diligence  
**Budget:** $100K–$500K/year (compliance budget, not technology budget)  
**Motion:** Direct outreach to CCOs; webinars on EU AI Act requirements; legal conference sponsorship  
**Volume:** Lower volume, highest ACV; most valuable customer type

### Segment 4: AI Model Providers (OEM / Partnership)
**Who:** Mistral, Cohere, Stability AI, OpenAI enterprise — model providers who want to offer customers documentation of safety testing  
**Pain:** Enterprise customers demand safety certifications before adopting a model  
**Motion:** BD partnership; RTaaS becomes a "certified" testing provider for the model provider ecosystem  
**Volume:** A few large deals that drive credibility and volume

---

## Pricing

### Starter (Freemium)
- 100 attacks/month free
- Static library only; no LLM mutation
- Basic JSON report only
- No compliance mapping
- Target: developers, researchers, early evaluation

### Professional — $299/month
- 5,000 attacks/month
- Static + dynamic mutation engine
- PDF + JSON reports
- EU AI Act and NIST RMF compliance mapping
- 3 attack profiles (general, financial, medical)
- Target: AI-native startups

### Business — $1,499/month
- 25,000 attacks/month
- All attack profiles (including legal, HR)
- Custom compliance frameworks
- Continuous monitoring mode (monthly re-test)
- Jira / ServiceNow integration
- Target: enterprise AI teams

### Enterprise — Custom ($5K–$50K/month)
- Unlimited attacks
- Custom attack library development
- White-label reporting
- Dedicated red-team support
- On-premises deployment option
- SLA: 48-hour report turnaround
- Target: financial institutions, large health systems, government

---

## Go-to-Market Strategy

### Channel 1: Developer Bottom-Up
- Open-source a limited version of the attack library on GitHub (marketing asset + community building)
- Submit to every AI tooling directory and newsletter
- Sponsor AI safety community forums (MLSEC, AI Alignment Forum)
- Developer documentation with tutorials for common use cases
- **Goal:** 500 free accounts in first 3 months

### Channel 2: Compliance Content Marketing
- Write definitive guides: "How to comply with EU AI Act Article 9 for LLM deployments"
- Partner with AI law firms for distribution
- Speaking at risk/compliance conferences (RIMS, ISACA)
- **Goal:** 50 qualified enterprise leads in first 6 months

### Channel 3: Research Credibility
- Publish methodology paper; release attack library dataset publicly
- Present at ACL, EMNLP, IEEE S&P
- **Goal:** Academic credibility that converts to enterprise trust

### Channel 4: Partner Channel
- System integrators (Accenture, Deloitte AI practices) looking for AI safety tooling to bundle with consulting
- **Goal:** 2 SI partner relationships in Year 1; 10x customer reach

---

## Financial Projections

| Quarter | ARR | Active Customers | Key Milestone |
|---------|-----|-----------------|---------------|
| Q2 2026 | $0 | Developer beta | Launch developer preview; 50 free accounts |
| Q3 2026 | $80K | 8 paid | EU AI Act enforcement begins; compliance pull starts |
| Q4 2026 | $300K | 30 paid | First enterprise contract; Series seed close |
| Q1 2027 | $700K | 70 paid | First model provider partnership |
| Q2 2027 | $1.5M | 150 paid | Series A positioning |
| Q4 2027 | $4M | 400 paid | 10 enterprise contracts at $100K+ |

**Unit Economics (Year 2 target):**
- CAC (blended): $3,500
- LTV (blended, 24-month): $14,000
- LTV/CAC: 4x

---

## Funding Strategy

**Bootstrap through initial commercialization** using existing open-source framework and minimal infrastructure costs. First customers fund further development.

**Seed Round ($1.5–2.5M):** Target Q4 2026 on $300K ARR traction  
- Purpose: 4 engineers, 1 sales, 1 legal/compliance specialist, infrastructure
- Investors: AI-focused seed funds (AIX Ventures, 1517 Fund, Conviction)

**Series A ($6–10M):** Target Q3 2027 on $4M ARR  
- Purpose: Scale sales team, expand attack library, build enterprise features, international

**Non-dilutive:** SBIR Phase I/II from DHS, DARPA (AI safety is a national security priority)

---

## Risks and Mitigations

| Risk | Details | Mitigation |
|------|---------|------------|
| Commoditization by OpenAI / Anthropic | Model providers could bundle safety evaluations into their APIs | Differentiate on multi-provider coverage, compliance reports, and domain specificity; model providers are motivated NOT to become adversarial red-teamers of each other |
| Garak / open-source wins | If Garak matures into a production tool, DIY adoption increases | RTaaS value is in compliance reports, not just attack execution; compliance reporting is not a feature Garak will prioritize |
| Liability for false negatives | If we say model is "safe" and it causes harm, are we liable? | Explicit "assessment not certification" language; security industry precedent (penetration testing firms face similar liability landscape) |
| Attack library goes stale | LLMs update constantly; yesterday's jailbreak may not work on today's model | Continuous dynamic mutation + community contributions keep library current |
| Regulation slows down | If EU AI Act enforcement is delayed, demand impulse weakens | Market is still growing on enterprise risk awareness even without hard enforcement |

---

*Symposium 2026 — Research Engineering Track*
