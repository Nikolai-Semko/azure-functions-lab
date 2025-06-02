# CST8917 Lab 1: Azure Functions with Output Bindings

This repository contains two Azure Function apps demonstrating output bindings for Azure Storage Queue and Azure SQL Database.

## 📹 Demo Video

[Watch the 5-minute demo on YouTube](https://youtu.be/hapWRmBGUho)


## Overview
This project demonstrates an HTTP-triggered Azure Function that writes messages to Azure Queue Storage. When you send a request with a name parameter, the function stores that name in a queue.

## Project Structure
```
azure-functions-lab/
└── StorageQueueFunction/
    ├── function_app.py      # Main function code
    ├── requirements.txt     # Python dependencies
    ├── host.json           # Function host configuration
    └── local.settings.json # Local configuration (not in repo)
```

## Prerequisites
- Python 3.8 to 3.11 (I used 3.10.11)
- Azure Functions Core Tools v4
- Visual Studio Code with Azure Functions extension
- Azure subscription (free tier works)

## Setup Instructions

### 1. Create Azure Storage Account
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → Search "Storage account"
3. Create with these settings:
   - **Name**: Choose unique name (e.g., `storageaccountlab1`)
   - **Region**: Select closest to you
   - **Performance**: Standard
   - **Redundancy**: LRS
4. After creation, go to "Access keys" and copy the connection string

### 2. Configure Local Settings
Create `local.settings.json` in the StorageQueueFunction folder:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "YOUR_STORAGE_CONNECTION_STRING",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing"
  }
}
```
Replace `YOUR_STORAGE_CONNECTION_STRING` with your actual connection string.

### 3. Install Dependencies
```bash
cd StorageQueueFunction
python -m venv .venv
.venv\Scripts\activate  # On Windows
# .venv/bin/activate    # On Mac/Linux
pip install -r requirements.txt
```

## Running the Function Locally

1. Start the function:
```bash
func start
```

2. You should see:
```
Functions:
    HttpExample: [GET,POST] http://localhost:7071/api/HttpExample
```

## Testing the Function

### Method 1: Browser
Open: `http://localhost:7071/api/HttpExample?name=YourName`

### Method 2: PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:7071/api/HttpExample?name=TestMessage"
```

### Method 3: curl
```bash
curl "http://localhost:7071/api/HttpExample?name=TestMessage"
```

## Verifying Queue Messages

### Azure Portal:
1. Go to your Storage Account
2. Click "Queues" in the left menu
3. Click on "outqueue"
4. You'll see your messages listed

### Azure Storage Explorer:
1. Connect to your storage account
2. Navigate to Queues → outqueue
3. View all messages sent by your function

## How It Works
1. HTTP request comes in with a `name` parameter
2. Function extracts the name from request
3. Function writes the name to "outqueue" using output binding
4. Azure automatically creates the queue if it doesn't exist
5. Message stays in queue until processed (default: 7 days)

## Troubleshooting
- **Port 7071 in use**: Kill the process using `taskkill /PID [processID] /F`
- **Storage connection error**: Verify your connection string in local.settings.json
- **No messages in queue**: Check function logs for errors

## What I Learned
- How to create and configure Azure Functions with Python
- Using output bindings to write to Queue Storage
- Difference between local development and Azure deployment
- How to test functions locally before deploying
- Azure Storage Explorer is useful for debugging