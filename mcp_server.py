from mcp.server.fastmcp import FastMCP
import httpx

# Instantiate the MCP server
mcp = FastMCP("Inventory Manager")

API_URL = "http://127.0.0.1:8000"

# Define the tools by calling the FastAPI endpoints
@mcp.tool()
def list_all_items() -> str:
    """Retrieves and lists all items currently in the inventory."""
    try:
        response = httpx.get(f"{API_URL}/items/")
        response.raise_for_status()
        return response.text
    except httpx.RequestError as e:
        return f"Error: Failed to connect to the FastAPI server: {e}"

@mcp.tool()
def add_new_item(name: str, quantity: int, price: float) -> str:
    """Adds a new item to the inventory with the specified name, quantity, and price."""
    try:
        item_data = {"name": name, "quantity": quantity, "price": price}
        response = httpx.post(f"{API_URL}/items/", json=item_data)
        response.raise_for_status()
        return response.text
    except httpx.RequestError as e:
        return f"Error: Failed to connect to the FastAPI server: {e}"
    except httpx.HTTPStatusError as e:
        return f"Error adding item: {e.response.json()['detail']}"

if __name__ == "__main__":
    mcp.run(transport="stdio")