# daily_fetch.sh
#!/bin/bash
source venv/bin/activate
python services/store_bills.py
