# GRC Control Mapper

Answer one self-assessment, see your coverage against **ISO/IEC 27001:2022**, **PCI DSS v4.0** and **NIST CSF 2.0** at the same time, with a prioritised gap list for each.

Many organisations answer the same control questions three times for three frameworks. This tool maps a common control set across all three so one assessment drives all three views.

## Quick start

No dependencies, just Python 3.8+.

```bash
python mapper.py sample_assessment.csv
python mapper.py sample_assessment.csv --out report.md
```

## How it works

1. `controls_map.csv` holds 22 common controls, each mapped to its Annex A / PCI DSS requirement / CSF subcategory references.
2. Your assessment CSV gives each control a status: `implemented`, `partial`, `not_implemented` or `not_applicable`.
3. The script scores coverage (1 / 0.5 / 0, N/A excluded) and lists gaps per framework.

Example output (from the fictional sample data):

```
| Framework          | Coverage |
| ISO/IEC 27001:2022 | 66.7%    |
| PCI DSS v4.0       | 66.7%    |
| NIST CSF 2.0       | 66.7%    |
```

The report then lists the gaps for each framework with the control, reference, status and notes.

## Extending it

Add rows to `controls_map.csv` (keep the same columns) and matching rows to your assessment file. Contributions that improve or extend the mapping are welcome.

## Disclaimer

The mapping is indicative and intended for self-assessment and prioritisation. It is not a substitute for the published standards or a formal audit. All sample data is fictional.

## Author

Papa, GRC, Risk & Cybersecurity Compliance Leader. [LinkedIn](https://www.linkedin.com/in/owoahene)
