# Methods

The native workflow uses DuckDB to query the raw CSV [@duckdb_csv].
The source combines billing and servicing provider identifiers,
the HCPCS procedure identifier, payment totals, claims, and aggregate
beneficiary counts. The annual result sums nominal payments and
claims by the calendar year of the reported month.

The archive replay pins a source revision and checks three artifact
digests, covering the exploratory summary, the annual table, and the
figure. It reconciles annual claim totals to the archived overall
record. The paid totals agree within two dollars across the different
aggregation orders. Decimal rounding gives the displayed billions
and trillions. Full commands are in the
[reproduction guide](https://github.com/docxology/hhs-opendata/blob/main/docs/reproduce.md).
