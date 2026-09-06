# Financial Model Gate

## Purpose

Build the model around a decision, not a fundraising narrative. Complete a decision-grade financial gate before detailed UX work: use an order-of-magnitude model to authorize only a cheap validation experiment, and a detailed monthly model before paid launch, permanent cost commitments, or acquisition scaling. Refresh the decision when UX, risk, architecture, pricing, or scope materially changes the economics.

Use `$product-financial-model` as the product-finance orchestrator when it is installed. It should gather and classify inputs, define product drivers and economic gates, then use the Spreadsheet skill to create an auditable workbook. The Spreadsheet skill remains responsible for workbook formulas, scenarios, sensitivities, checks, and file verification. Neither skill replaces accounting, tax, or legal review.

## Early viability checkpoint

Complete a preliminary review before Gate 5 scope approval for every project. For commercial products, start once a working Gate 1 segment exists and test market volume, reachable demand, acquisition mechanisms, channel capacity, CAC, contribution, fixed cost, and a Month-24 profit path. Broad ranges are acceptable only when every material unknown has an evidence class and a cheap validation plan.

If the owner has not selected a different meaningful target or currency, use **RUB 1 million sustainable monthly operating profit by Month 24** as the default. Require a trailing-three-month average, include acquisition and recurring operating costs, show tax treatment, seasonality, peak burn, and cash need, and do not use unvalidated future revenue to pass.

Report how plausible the target is with scenario coverage, channel/market/cash headroom, and evidence maturity. Do not invent a probability of success from unsupported assumptions. Non-commercial products must record why profit is not applicable and use an explicit cost/value or capacity constraint.

## 1. Model brief

Record:

- decision to make;
- currency, taxes, legal entity, and as-of date;
- monthly horizon of at least 24 months for cash planning;
- unit of economics: user, payer, order, group, transaction, or another atomic unit;
- owner and next recalculation date or trigger.

## 2. Driver tree

Start with causality:

```text
traffic
→ registration
→ activation
→ retained user
→ payer or purchase
→ revenue
→ variable cost
→ contribution
→ fixed cost
→ operating result and cash
```

Give every arrow a formula, unit, time window, source, and metric owner.

## 3. Inputs to collect

### Audience and funnel

- impressions, clicks, CPC/CPM;
- registration and registration CAC;
- activation and activated-user CAC;
- MAU, retention, and frequency;
- trial, free-to-paid, purchase conversion;
- payer churn, refunds, and payment failures.

### Revenue

- monthly and annual prices and mix;
- transactions and one-time purchases;
- advertising reach, sessions, impressions, fill rate, and net eCPM;
- affiliate, CPA/CPS/CPL, sponsorship, and B2B streams.

Model each stream separately. Do not use unvalidated partnership revenue to hide weak subscription economics.

### Variable costs

- payment fees, tax on fees, receipts, refunds, and chargebacks;
- AI, APIs, storage, traffic, messages, and support per action or user;
- partner share, licensing, fulfillment, and moderation;
- free trials, welcome credits, and other consumable free usage.

### Fixed, step, and one-time costs

- product, engineering, QA, DevOps, support, sales, and administration;
- editorial, design, photography, and content;
- servers, database, storage, monitoring, backup, and security;
- legal, privacy, accounting, brand, initial development, migration, and launch;
- thresholds where team or infrastructure cost increases in a step;
- founder compensation or an explicit temporary exclusion;
- cash reserve and payment-collection delays.

## 4. Evidence quality

Classify each material input:

| Status | Meaning |
|---|---|
| Fact | Contract, invoice, or official current tariff |
| Observed | Product analytics, payments, experiment, or support data |
| Benchmark | External comparable range; not a target or promise |
| Hypothesis | Team assumption with owner, range, and test |
| Unknown | No defensible value; use a range and collection plan |

Store URL, date, geography, category, sample, and applicability for external data. Replace hypotheses with observed cohorts after launch.

## 5. Workbook structure

Use:

1. Dashboard
2. Assumptions
3. Revenue Drivers
4. Cost Model
5. Acquisition
6. P&L
7. Cash Flow
8. Scenarios and Sensitivity
9. Sources
10. Checks

Keep inputs editable and calculations formula-driven. Do not hardcode desired outputs.

## 6. Required formulas

```text
Payers = MAU × paid conversion

Blended ARPPU = monthly price × monthly mix
              + annual price / 12 × annual mix

Net ARPPU = Blended ARPPU
          × (1 - refunds)
          × (1 - payment costs)

Contribution / payer = Net ARPPU
                     - variable product cost
                     - variable support cost

CAC = channel spend / acquired users at the named funnel stage

Contribution LTV = contribution per payer / monthly payer churn

Allowable CAC = Contribution LTV / target LTV-to-CAC

Runway = available cash / average monthly net burn
```

Also calculate gross and net revenue, gross/contribution margin, payback, break-even users or paid share, operating result, burn, and cash balance. Use cohort cash flow instead of simple LTV when annual plans, retention changes, or long payback make the shortcut misleading.

## 7. Scenarios and sensitivity

Build:

- conservative: lower price/conversion and higher churn/CAC/cost;
- base: most likely values with rationale;
- optimistic: strong but achievable values.

Test price, annual mix, paid conversion, retention/churn, channel CAC, AI or other consumable cost, payment fees, refunds, partner share, major fixed costs, MAU, and ad ARPU where applicable. Record the break point and early-warning metric for each major driver.

## 8. Audit

Confirm:

- component totals tie;
- free plus paid users reconcile to the population;
- annual prices convert to months correctly;
- revenue and associated costs use the same period;
- payment, tax, refund, free-credit, and support costs are included;
- no revenue or cost is double-counted;
- zero and negative cases are guarded;
- outputs trace to sources;
- formula-error scan and visible checks pass;
- the workbook is readable and assumptions recalculate without manual edits.

## 9. Decision gates

- **Early viability before scope:** market, acquisition, unit-economics, and Month-24 ranges support proceed, cheaper experiment, change, or stop.
- **Prototype:** broad ranges are acceptable when validation is cheap.
- **Paid pilot:** payment flow, variable cost, refunds, and willingness to pay have evidence.
- **Permanent hiring/content:** retention, repeat value, and plausible break-even are evidenced.
- **Acquisition scaling:** observed contribution LTV exceeds channel CAC by the chosen margin and payback fits runway.

Finish with one decision: proceed, run a cheaper experiment, change price or scope, reduce fixed cost, reject a channel, or stop. Recalculate after changes to pricing, monetization, major scope, architecture, or mature retention/payment cohorts.
