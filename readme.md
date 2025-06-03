# Azure Functions Lab

This repository contains Azure Functions created as part of a lab exercise demonstrating serverless computing with Azure Functions and Azure SQL Database integration.

## 📹 Demo Video

[Watch the 5-minute demo on YouTube](https://youtu.be/hAErAQAwXW0)

## Lab Objectives

This lab demonstrates:
- Creating and deploying Azure Functions using Visual Studio Code
- Implementing HTTP triggers
- Integrating Azure Functions with Azure SQL Database
- Using output bindings to write data to SQL Database

## Project Structure

```
azure-functions-lab/
├── HttpTriggerFunction/       # Part 1: Basic HTTP Trigger Function
│   ├── function_app.py
│   ├── local.settings.json
│   └── requirements.txt
└── SQLDatabaseFunction/       # Part 2: SQL Database Integration
    ├── function_app.py
    ├── local.settings.json
    └── requirements.txt
```

## Part 1: Basic HTTP Trigger Function

### Prerequisites
- Python 3.8 to 3.11 (I used 3.10.11)
- Azure Functions Core Tools v4
- Visual Studio Code with Azure Functions extension
- Azure subscription (free tier works)
- Azure SQL Database (for Part 2)

### Setup Instructions

#### 1. Create Azure Storage Account
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → Search "Storage account"
3. Create with these settings:
   - **Name**: Choose unique name (e.g., `storageaccountlab1`)
   - **Region**: Select closest to you
   - **Performance**: Standard
   - **Redundancy**: LRS
4. After creation, go to "Access keys" and copy the connection string

#### 2. Configure Local Settings
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

#### 3. Install Dependencies
```bash
cd StorageQueueFunction
python -m venv .venv
.venv\Scripts\activate  # On Windows
# .venv/bin/activate    # On Mac/Linux
pip install -r requirements.txt
```

### Running the Function Locally

1. Start the function:
```bash
func start
```

2. You should see:
```
Functions:
    HttpExample: [GET,POST] http://localhost:7071/api/HttpExample
```

### Testing the Function

#### Method 1: Browser
Open: `http://localhost:7071/api/HttpExample?name=YourName`

#### Method 2: PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:7071/api/HttpExample?name=TestMessage"
```

#### Method 3: curl
```bash
curl "http://localhost:7071/api/HttpExample?name=TestMessage"
```

### Verifying Queue Messages

#### Azure Portal:
1. Go to your Storage Account
2. Click "Queues" in the left menu
3. Click on "outqueue"
4. You'll see your messages listed

#### Azure Storage Explorer:
1. Connect to your storage account
2. Navigate to Queues → outqueue
3. View all messages sent by your function

### How It Works
1. HTTP request comes in with a `name` parameter
2. Function extracts the name from request
3. Function writes the name to "outqueue" using output binding
4. Azure automatically creates the queue if it doesn't exist
5. Message stays in queue until processed (default: 7 days)

### Troubleshooting
- **Port 7071 in use**: Kill the process using `taskkill /PID [processID] /F`
- **Storage connection error**: Verify your connection string in local.settings.json
- **No messages in queue**: Check function logs for errors

### What I Learned
- How to create and configure Azure Functions with Python
- Using output bindings to write to Queue Storage
- Difference between local development and Azure deployment
- How to test functions locally before deploying
- Azure Storage Explorer is useful for debugging

## Part 2: SQL Database Integration

### Overview
An enhanced HTTP-triggered Azure Function that writes todo items to an Azure SQL Database using output bindings.

### Features
- HTTP trigger with anonymous authentication
- SQL output binding for database writes
- Accepts JSON payload with todo item details
- Automatically generates unique IDs for each item
- Supports optional fields (url, order)

### Database Schema
```sql
CREATE TABLE dbo.ToDo (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY,
    [order] INT NULL,
    [title] NVARCHAR(200) NOT NULL,
    [url] NVARCHAR(200) NOT NULL,
    [completed] BIT NOT NULL
);
```

### Request Format
```json
{
    "name": "Todo Item Title",
    "url": "https://example.com",  // optional
    "order": 1                      // optional
}
```

### Testing Part 2
```powershell
# Using PowerShell
Invoke-RestMethod -Uri "http://localhost:7071/api/sqltrigger" -Method POST -ContentType "application/json" -Body '{"name":"Test Item","url":"www.beexxl.com","order":69}'

# Using curl (in Command Prompt)
curl -X POST http://localhost:7071/api/sqltrigger -H "Content-Type: application/json" -d "{\"name\":\"Test Item\"}"
```

### Setup Instructions

1. Create an Azure SQL Database
2. Configure connection string in `local.settings.json`:
   ```json
   {
     "Values": {
       "SqlConnectionString": "Your-ADO.NET-Connection-String"
     }
   }
   ```
3. Create the ToDo table in your database
4. Navigate to `SQLDatabaseFunction` directory
5. Follow steps 3-6 from Part 1 setup

### Deployment

#### Using VS Code
1. Press F1 and select "Azure Functions: Deploy to Function App"
2. Select your subscription and function app
3. Confirm deployment

#### Using Azure Functions Core Tools
```bash
func azure functionapp publish <FunctionAppName>
```

### Troubleshooting

1. **JSON Parse Error**: Ensure request body contains valid JSON
2. **Connection String Error**: Verify SQL connection string in settings
3. **Authentication Error**: Check database firewall rules allow Azure services
