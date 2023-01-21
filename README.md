master branch CI\
[![crypto-price-tool](https://github.com/rogerkupari/crypto-price-tool/actions/workflows/python-app.yml/badge.svg?branch=master&event=push)](https://github.com/rogerkupari/crypto-price-tool/actions/workflows/python-app.yml)

dev branch CI\
[![crypto-price-tool](https://github.com/rogerkupari/crypto-price-tool/actions/workflows/python-app.yml/badge.svg?branch=dev&event=push)](https://github.com/rogerkupari/crypto-price-tool/actions/workflows/python-app.yml)


**Usage**:python3 crypto_price_tool.py --binance <path to binance account report> --output <path to output file> \
e.g: python3 crypto_price_tool.py --binance binance_latest.csv --output price_report.xlsx \
\
**Note**: number of CoinGecko requests are limited against time, so it can take some time to process.
