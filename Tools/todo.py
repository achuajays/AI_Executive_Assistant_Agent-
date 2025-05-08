from smolagents import Tool
import requests
import json


class TodoManagerTool(Tool):
    name = "todo_manager"
    description = (
        "Manages todo items by interacting with the specified API. Supports creating, retrieving, "
        "updating, and deleting todo items. Returns responses as JSON strings."
    )

    inputs = {
        "operation": {
            "type": "string",
            "description": "The operation to perform: 'create', 'retrieve', 'update', or 'delete'."
        },
        "title": {
            "type": "string",
            "description": "The title of the todo item (required for 'create' and 'update').",
            "default": None,
            "nullable": True
        },
        "description": {
            "type": "string",
            "description": "The description of the todo item (required for 'create' and 'update').",
            "default": None,
            "nullable": True
        },
        "completed": {
            "type": "boolean",
            "description": "The completion status of the todo item (default: false for 'create' and 'update').",
            "default": False,
            "nullable": True
        },
        "id": {
            "type": "integer",
            "description": "The ID of the todo item (required for 'update' and 'delete').",
            "default": None,
            "nullable": True
        },
        "skip": {
            "type": "integer",
            "description": "Number of items to skip for pagination (default: 0 for 'retrieve').",
            "default": 0,
            "nullable": True
        },
        "limit": {
            "type": "integer",
            "description": "Maximum number of items to return (default: 100 for 'retrieve').",
            "default": 100,
            "nullable": True
        }
    }

    output_type = "string"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://aiexecutiveassistantagent-production.up.railway.app/todos/"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        self.delete_headers = {
            "accept": "*/*"
        }

    def forward(self, operation: str, title: str = None, description: str = None,
                completed: bool = False, id: int = None, skip: int = 0, limit: int = 100) -> str:
        """
        Perform the specified todo operation.

        Args:
            operation (str): The operation to perform ('create', 'retrieve', 'update', 'delete').
            title (str, optional): The title of the todo item (for 'create', 'update').
            description (str, optional): The description of the todo item (for 'create', 'update').
            completed (bool, optional): The completion status (for 'create', 'update').
            id (int, optional): The ID of the todo item (for 'update', 'delete').
            skip (int, optional): Number of items to skip (for 'retrieve').
            limit (int, optional): Maximum number of items to return (for 'retrieve').

        Returns:
            str: A JSON string of the API response or an error message.
        """
        # Validate operation
        valid_operations = {"create", "retrieve", "update", "delete"}
        if operation not in valid_operations:
            return f"Error: Invalid operation. Must be one of {valid_operations}."

        try:
            if operation == "create":
                # Validate inputs for create
                if not title or not isinstance(title, str):
                    return "Error: Title must be a non-empty string for create operation."
                if not description or not isinstance(description, str):
                    return "Error: Description must be a non-empty string for create operation."
                if not isinstance(completed, bool):
                    return "Error: Completed must be a boolean for create operation."

                # Construct payload
                payload = {
                    "title": title.strip(),
                    "description": description.strip(),
                    "completed": completed
                }

                # Send POST request
                response = requests.post(self.base_url, headers=self.headers, json=payload)
                response.raise_for_status()
                return json.dumps(response.json(), indent=2)

            elif operation == "retrieve":
                # Validate inputs for retrieve
                if not isinstance(skip, int) or skip < 0:
                    return "Error: Skip must be a non-negative integer for retrieve operation."
                if not isinstance(limit, int) or limit < 1:
                    return "Error: Limit must be a positive integer for retrieve operation."

                # Construct query parameters
                querystring = {"skip": str(skip), "limit": str(limit)}

                # Send GET request
                response = requests.get(self.base_url, headers=self.headers, params=querystring)
                response.raise_for_status()
                return json.dumps(response.json(), indent=2)

            elif operation == "update":
                # Validate inputs for update
                if id is None or not isinstance(id, int) or id < 1:
                    return "Error: ID must be a positive integer for update operation."
                if not title or not isinstance(title, str):
                    return "Error: Title must be a non-empty string for update operation."
                if not description or not isinstance(description, str):
                    return "Error: Description must be a non-empty string for update operation."
                if not isinstance(completed, bool):
                    return "Error: Completed must be a boolean for update operation."

                # Construct payload
                payload = {
                    "title": title.strip(),
                    "description": description.strip(),
                    "completed": completed
                }

                # Construct URL with ID
                url = f"{self.base_url}{id}"

                # Send PUT request
                response = requests.put(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return json.dumps(response.json(), indent=2)

            elif operation == "delete":
                # Validate inputs for delete
                if id is None or not isinstance(id, int) or id < 1:
                    return "Error: ID must be a positive integer for delete operation."

                # Construct URL with ID
                url = f"{self.base_url}{id}"

                # Send DELETE request
                response = requests.delete(url, headers=self.delete_headers)
                response.raise_for_status()
                # DELETE may return no content (204), so return a success message
                if response.status_code == 204:
                    return json.dumps({"message": f"Todo item with ID {id} deleted successfully"}, indent=2)
                return json.dumps(response.json(), indent=2)

        except requests.RequestException as e:
            return f"Error performing {operation} operation: {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid JSON response from the API."
        except Exception as e:
            return f"Error processing request: {str(e)}"