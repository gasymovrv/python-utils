# Python Utilities Collection

A collection of useful Python utilities for various tasks including file encryption, Excel data analysis, email sending, and SQL database operations.

## Project Structure

- **encrypt/** - File encryption and decryption utilities using AES-256
  - `encrypt_file.py` - Encrypts files using AES-256 in GCM mode with PBKDF2 key derivation
  - `decrypt_file.py` - Decrypts files encrypted with the encrypt_file.py script

- **xls/** - Excel data analysis utilities
  - `headache_stats.py` - Analyzes headache data from Excel files and generates statistical visualizations
  - `money_manager_stats.py` - Analyzes financial data from Excel files

- **email/** - Email sending utilities
  - `send_test_emails.py` - Sends test emails
  - `send_emails_by_STAGE_smtp.py` - Sends test emails via SMTP server with attachments

- **sql/customer_requests/** - SQL database visualization tools
  - `histogram.py` - Generates histograms from PostgreSQL database queries
  - `chart.py` - Generates charts from database queries
  - `chart2.py` - Additional charting functionality

## Installation

1. Clone this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Dependencies

- psycopg2 - PostgreSQL database adapter
- matplotlib - Data visualization library
- openpyxl - Excel file manipulation
- requests - HTTP library
- pandas - Data analysis and manipulation
- pycryptodome - Cryptographic library

## Usage Examples

### File Encryption

```shell
# Encrypt a file
python encrypt/encrypt_file.py <input_file> <password>

# Decrypt a file
python encrypt/decrypt_file.py <encrypted_file> <password>
```

### Excel Data Analysis

```shell
# Analyze headache statistics
python xls/headache_stats.py

# Analyze financial data
python xls/money_manager_stats.py
```

### Email Sending

```shell
# Send test emails
python email/send_test_emails.py

# Send test emails with attachments via SMTP
python email/send_emails_by_STAGE_smtp.py
```

### Database Operations

```shell
# Generate histogram from database data
python sql/customer_requests/histogram.py

# Generate charts from database data
python sql/customer_requests/chart.py
python sql/customer_requests/chart2.py
```

## Notes

- Before using email utilities, update the SMTP server credentials and recipient information
- For SQL database utilities, update the database connection information
- For Excel data analysis, make sure to update file paths in the scripts

