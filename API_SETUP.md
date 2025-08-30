# API Setup Guide for SuperPerformanceScreener

This guide will walk you through setting up all the required API keys and credentials for the SuperPerformanceScreener.

## 🔑 Required API Keys

You need **2 main API keys** to run the SuperPerformanceScreener:

1. **EODHD API Key** - For real-time stock data and analysis
2. **Google Sheets API Credentials** - For outputting results to spreadsheets

---

## 1. EODHD API Key Setup

### Step 1: Create EODHD Account
1. Go to [EODHD](https://eodhd.com/register)
2. Click "Sign Up" and create a free account
3. Verify your email address

### Step 2: Get API Key
1. Go to [EODHD Dashboard](https://eodhd.com/dashboard)
2. Click "API Keys" in the left sidebar
3. Copy your API key (starts with your username)

### Step 3: Add to Environment
1. Copy `env_example.txt` to `.env`:
   ```bash
   cp env_example.txt .env
   ```
2. Edit `.env` and add your EODHD API key:
   ```
   EODHD_API_KEY=your_eodhd_api_key_here
   ```

### Step 4: Verify Setup
Test your API key:
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('EODHD API Key:', os.getenv('EODHD_API_KEY')[:10] + '...' if os.getenv('EODHD_API_KEY') else 'Not found')
"
```

---

## 2. Google Sheets API Setup

### Option A: Service Account (Recommended)

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "SuperPerformanceScreener" and click "Create"

#### Step 2: Enable Google Sheets API
1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"

#### Step 3: Create Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in:
   - **Service account name**: `superperformance-screener`
   - **Service account ID**: auto-generated
   - **Description**: `Service account for SuperPerformanceScreener`
4. Click "Create and Continue"
5. Skip role assignment (click "Continue")
6. Click "Done"

#### Step 4: Generate Credentials
1. Click on your new service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Click "Create" - this downloads `credentials.json`

#### Step 5: Set Up Credentials
1. Move `credentials.json` to your project root directory
2. Add to `.env`:
   ```
   GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
   ```

#### Step 6: Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new blank spreadsheet
3. Copy the Spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```
4. Add to `.env`:
   ```
   GOOGLE_SHEETS_SPREADSHEET_ID=your-spreadsheet-id-here
   ```

#### Step 7: Share Sheet with Service Account
1. In your Google Sheet, click "Share"
2. Add the service account email (found in `credentials.json` under `client_email`)
3. Give it "Editor" permissions
4. Click "Send"

### Option B: OAuth2 (Alternative)

If you prefer OAuth2 authentication:

1. Follow steps 1-2 from Service Account setup
2. Create OAuth2 credentials instead of Service Account
3. Download OAuth2 credentials and set up OAuth2 flow
4. The system will prompt for authentication on first run

---

## 3. Final Configuration

### Complete .env File
Your `.env` file should look like this:
```bash
# EODHD API Configuration
EODHD_API_KEY=your-actual-eodhd-api-key-here

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your-actual-spreadsheet-id-here
```

### Test Your Setup
Run the demo to verify everything works:
```bash
python demo.py
```

---

## 4. Usage Examples

### Basic Usage
```bash
# Run with default settings
python main.py

# Run in test mode (uses sample stocks)
python main.py --test

# Run with custom parameters
python main.py --max-stocks 100
```

### Advanced Usage
```bash
# Use custom API keys
python main.py --eodhd-key YOUR_KEY --spreadsheet-id YOUR_SHEET_ID

# Run with specific stocks
python main.py --max-stocks 50 --test
```



You're ready to run the SuperPerformanceScreener! Start with:

```bash
python main.py --test
```

This will analyze sample stocks and output results to your Google Sheet. 
