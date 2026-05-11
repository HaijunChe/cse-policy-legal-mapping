# CSE Policy & Legal Environment — 8 Country Snapshot

**Interactive dashboard** mapping the policy and legal environment for Comprehensive Sexuality Education (CSE) across 8 countries spanning Africa, Asia, and Latin America.

Built as a homework assignment for the UNFPA Data Analytics and Visualization Consultancy (GHRIB/PD CSE Team).

## Live Dashboard

**[View the dashboard →](https://haijunche.github.io/cse-policy-mapping/)**

## Coverage

### Countries (8)
| Region | Countries |
|--------|-----------|
| Eastern Africa | Kenya, Ethiopia |
| Western Africa | Nigeria |
| Southern Africa | South Africa |
| South-Eastern Asia | Indonesia, Philippines |
| South America | Colombia, Argentina |

### Dimensions Mapped
1. **CSE in Education Systems**
   - Integration into school curricula (Yes / Partial / No)
   - Local naming / framing (CSE, Life Skills, FLHE, ESI, etc.)

2. **Age of Consent Laws**
   - Legal threshold by country
   - Notes on complexity (federal systems, close-in-age exemptions, etc.)

3. **GBV Legal Framework**
   - Existence of comprehensive legislation
   - Key laws and policy context

## Data Sources

All data points are sourced from publicly available, authoritative sources:

- **UNESCO GEM Report** — CSE Country Profiles (2023)
- **PEER Education Profiles** — education-profiles.org
- **UN Women Global Database on Violence Against Women** — evaw-global-database.unwomen.org
- **World Bank** — Women, Business and the Law 2024
- **National legislation** — official government publications

## Technology Stack

- **HTML5** + **CSS3** (no build step)
- **Leaflet.js** — interactive mapping
- **OpenStreetMap** — base tiles
- Vanilla JavaScript (ES6+)

## Key Design Decisions

- **No build step / bundler** — ensures fast load times and easy maintainability
- **Client-side data** — all country data loaded from a single JSON file for transparency
- **Every data point cited** — source links are embedded in the detail panel
- **Limitations are explicit** — methodology section notes law-vs-practice gaps, sub-national variation, and comparability issues

## Local Development

```bash
# Start a local server
python -m http.server 8080

# Open in browser
open http://localhost:8080
```

## Author

Haijun Che — Data Analytics & Visualization Consultant applicant
