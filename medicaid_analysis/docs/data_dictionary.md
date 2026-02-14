# Data Dictionary

## Source Dataset

**File**: `data/medicaid-provider-spending.csv`  
**Source**: CMS (Centers for Medicare & Medicaid Services) — Medicaid Provider Utilization  
**Granularity**: One row per (billing provider × servicing provider × HCPCS code × month)

## Column Definitions

| Column | Type | Description |
|---|---|---|
| `CLAIM_FROM_MONTH` | `VARCHAR` | Service month in `YYYY-MM` format (e.g., `2018-01`) |
| `BILLING_PROVIDER_NPI_NUM` | `VARCHAR` | National Provider Identifier of the billing entity |
| `SERVICING_PROVIDER_NPI_NUM` | `VARCHAR` | National Provider Identifier of the servicing entity |
| `HCPCS_CODE` | `VARCHAR` | Healthcare Common Procedure Coding System code |
| `TOTAL_PAID` | `FLOAT` | Total Medicaid payment amount (USD) for this row |
| `TOTAL_CLAIMS` | `INTEGER` | Total number of claims for this row |
| `TOTAL_UNIQUE_BENEFICIARIES` | `INTEGER` | Unique Medicaid beneficiaries served |

## Full Dataset Statistics

| Metric | Value |
|---|---|
| Total Rows | 227,083,361 |
| Total Paid | $1,093,562,833,510.64 |
| Total Claims | 18,825,564,012 |
| Unique Billing NPIs | 617,503 |
| Unique Servicing NPIs | 1,627,362 |
| Unique HCPCS Codes | 10,881 |

## Derived Metrics

Common computed columns used across analysis sections:

| Metric | Formula | Used In |
|---|---|---|
| Cost per Claim | `TOTAL_PAID / TOTAL_CLAIMS` | S05, S06, S17, S33, S37 |
| Cost per Beneficiary | `TOTAL_PAID / TOTAL_UNIQUE_BENEFICIARIES` | S05, S19 |
| Claims per Beneficiary | `TOTAL_CLAIMS / TOTAL_UNIQUE_BENEFICIARIES` | S19, S35 |
| Provider HHI | `Σ(code_share²)` per provider | S27 |
| Gini Coefficient | Lorenz area ratio | S08 |
| Spike Ratio | `monthly_paid / rolling_3mo_mean` | S34 |
| Z-Score | `(value - mean) / std` | S06, S33, S34 |

## HCPCS Code Categories

| Prefix | Category | Examples |
|---|---|---|
| `99xxx` | E&M (Evaluation & Management) | Office visits, consultations |
| `Txxxx` | State-Specific Codes | State-defined services |
| `Sxxxx` | Commercial Payer Codes | Non-Medicare services |
| `Jxxxx` | Drug Administration | Injectable drugs |
| `Hxxxx` | Behavioral Health | Mental health, substance abuse |
| `Gxxxx` | Temporary Procedures | CMS temporary codes |
| `Axxxx` | Transport & Supplies | Ambulance, medical supplies |
| `Dxxxx` | Dental | Dental procedures |
| `10004–69990` | Surgery | Surgical procedures |
| `70010–79999` | Radiology | Imaging & radiation |
| `80047–89398` | Pathology/Lab | Laboratory tests |
