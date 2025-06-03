import azure.functions as func
import logging
from azure.functions.decorators.core import DataType
import uuid

app = func.FunctionApp()

@app.function_name(name="SqlTrigger")
@app.route(route="sqltrigger", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_output_binding(arg_name="toDoItems", 
                           type="sql", 
                           CommandText="dbo.ToDo",
                           ConnectionStringSetting="SqlConnectionString",
                           data_type=DataType.STRING)
def SqlTrigger(req: func.HttpRequest, toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Try to get name from JSON body
    name = None
    try:
        req_body = req.get_json()
        if req_body:
            name = req_body.get('name')
    except ValueError:
        # No valid JSON in request
        pass
    
    if name:
        # Write to SQL Database
        toDoItems.set(func.SqlRow({
            "Id": str(uuid.uuid4()),
            "title": name,
            "completed": False,
            "url": ""
        }))
        return func.HttpResponse(f"Hello {name}! Your todo item has been saved.")
    else:
        return func.HttpResponse(
            "Please pass a name in the request body",
            status_code=400
        )