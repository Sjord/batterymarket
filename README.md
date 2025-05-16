# Battery Market Automation

This project fetches electricity spot prices for the Netherlands from the ENTSO-E Transparency Platform and calculates a battery charge level based on the current hour's price. The battery charge level is then written to your system via `bclm`.

## Requirements

- Python 3.9+
- `requests` package
- `bclm` command-line tool installed at `/usr/local/bin/bclm`
