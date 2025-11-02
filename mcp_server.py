#!/usr/bin/env python3
"""
MCP Server for DH Art Backend
Provides MCP tools for interacting with the WooCommerce backend API
"""

import asyncio
import os
from typing import Any, Optional
import httpx
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
API_BASE = f"{BACKEND_URL}/api"

# Initialize MCP server
server = Server("dhart-backend")


# Helper function to make API calls
async def make_api_call(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None
) -> dict:
    """Make an HTTP call to the backend API"""
    url = f"{API_BASE}{endpoint}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, json=data, params=params)
            elif method.upper() == "PUT":
                response = await client.put(url, json=data, params=params)
            elif method.upper() == "DELETE":
                response = await client.delete(url, params=params)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}

            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP {e.response.status_code}",
                "message": str(e),
                "details": e.response.text
            }
        except Exception as e:
            return {"error": str(e)}


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="dhart://health",
            name="Backend Health Status",
            description="Current health status of the DH Art backend",
            mimeType="application/json",
        ),
        Resource(
            uri="dhart://config",
            name="Backend Configuration",
            description="Configuration and environment information",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific resource"""
    if uri == "dhart://health":
        result = await make_api_call("GET", "/health")
        return str(result)
    elif uri == "dhart://config":
        result = await make_api_call("GET", "/config")
        return str(result)
    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        # Products tools
        Tool(
            name="list_products",
            description="List all products with optional filtering, pagination and sorting",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {"type": "number", "description": "Page number for pagination"},
                    "per_page": {"type": "number", "description": "Items per page (max 100)"},
                    "search": {"type": "string", "description": "Search term"},
                    "category": {"type": "string", "description": "Filter by category ID"},
                    "status": {"type": "string", "description": "Filter by status (publish, draft, etc.)"},
                    "featured": {"type": "boolean", "description": "Filter featured products"},
                    "on_sale": {"type": "boolean", "description": "Filter products on sale"},
                    "min_price": {"type": "string", "description": "Minimum price filter"},
                    "max_price": {"type": "string", "description": "Maximum price filter"},
                    "orderby": {"type": "string", "description": "Sort by (date, id, title, price)"},
                    "order": {"type": "string", "description": "Order direction (asc, desc)"},
                    "minimal": {"type": "boolean", "description": "Return minimal product data"},
                },
            },
        ),
        Tool(
            name="get_product",
            description="Get a specific product by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Product ID"},
                    "raw": {"type": "boolean", "description": "Return raw WooCommerce data"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="create_product",
            description="Create a new product",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Product name"},
                    "type": {"type": "string", "description": "Product type (simple, variable, etc.)"},
                    "regular_price": {"type": "string", "description": "Regular price"},
                    "sale_price": {"type": "string", "description": "Sale price"},
                    "description": {"type": "string", "description": "Product description"},
                    "short_description": {"type": "string", "description": "Short description"},
                    "categories": {"type": "array", "description": "Array of category objects with id"},
                    "images": {"type": "array", "description": "Array of image objects with src"},
                    "status": {"type": "string", "description": "Product status (draft, publish, etc.)"},
                },
                "required": ["name", "type", "regular_price"],
            },
        ),
        Tool(
            name="update_product",
            description="Update an existing product",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Product ID"},
                    "name": {"type": "string", "description": "Product name"},
                    "regular_price": {"type": "string", "description": "Regular price"},
                    "sale_price": {"type": "string", "description": "Sale price"},
                    "description": {"type": "string", "description": "Product description"},
                    "short_description": {"type": "string", "description": "Short description"},
                    "status": {"type": "string", "description": "Product status"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="delete_product",
            description="Delete a product by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Product ID"},
                    "force": {"type": "boolean", "description": "Force permanent deletion"},
                },
                "required": ["id"],
            },
        ),

        # Categories tools
        Tool(
            name="list_categories",
            description="List all product categories with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {"type": "number", "description": "Page number"},
                    "per_page": {"type": "number", "description": "Items per page"},
                    "search": {"type": "string", "description": "Search term"},
                    "parent": {"type": "string", "description": "Filter by parent category ID"},
                    "hide_empty": {"type": "boolean", "description": "Hide empty categories"},
                    "orderby": {"type": "string", "description": "Sort by (name, slug, count)"},
                    "order": {"type": "string", "description": "Order direction (asc, desc)"},
                },
            },
        ),
        Tool(
            name="get_category",
            description="Get a specific category by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Category ID"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="create_category",
            description="Create a new product category",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Category name"},
                    "slug": {"type": "string", "description": "Category slug"},
                    "parent": {"type": "number", "description": "Parent category ID"},
                    "description": {"type": "string", "description": "Category description"},
                    "image": {"type": "object", "description": "Image object with src"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="update_category",
            description="Update an existing category",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Category ID"},
                    "name": {"type": "string", "description": "Category name"},
                    "slug": {"type": "string", "description": "Category slug"},
                    "description": {"type": "string", "description": "Category description"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="delete_category",
            description="Delete a category by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Category ID"},
                    "force": {"type": "boolean", "description": "Force permanent deletion"},
                },
                "required": ["id"],
            },
        ),

        # Orders tools
        Tool(
            name="list_orders",
            description="List all orders with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {"type": "number", "description": "Page number"},
                    "per_page": {"type": "number", "description": "Items per page"},
                    "search": {"type": "string", "description": "Search term"},
                    "status": {"type": "string", "description": "Filter by order status"},
                    "customer": {"type": "string", "description": "Filter by customer ID"},
                    "product": {"type": "string", "description": "Filter by product ID"},
                    "after": {"type": "string", "description": "Filter orders after date (ISO8601)"},
                    "before": {"type": "string", "description": "Filter orders before date (ISO8601)"},
                },
            },
        ),
        Tool(
            name="get_order",
            description="Get a specific order by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Order ID"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="create_order",
            description="Create a new order",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {"type": "number", "description": "Customer ID"},
                    "line_items": {"type": "array", "description": "Array of line items"},
                    "billing": {"type": "object", "description": "Billing address object"},
                    "shipping": {"type": "object", "description": "Shipping address object"},
                    "payment_method": {"type": "string", "description": "Payment method ID"},
                    "payment_method_title": {"type": "string", "description": "Payment method title"},
                    "status": {"type": "string", "description": "Order status"},
                },
                "required": ["line_items"],
            },
        ),
        Tool(
            name="update_order",
            description="Update an existing order",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Order ID"},
                    "status": {"type": "string", "description": "Order status"},
                    "billing": {"type": "object", "description": "Billing address"},
                    "shipping": {"type": "object", "description": "Shipping address"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="get_order_notes",
            description="Get notes for a specific order",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Order ID"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="add_order_note",
            description="Add a note to an order",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Order ID"},
                    "note": {"type": "string", "description": "Note content"},
                    "customer_note": {"type": "boolean", "description": "Is customer note"},
                },
                "required": ["id", "note"],
            },
        ),

        # Customers tools
        Tool(
            name="list_customers",
            description="List all customers with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {"type": "number", "description": "Page number"},
                    "per_page": {"type": "number", "description": "Items per page"},
                    "search": {"type": "string", "description": "Search term"},
                    "email": {"type": "string", "description": "Filter by email"},
                    "role": {"type": "string", "description": "Filter by role"},
                    "orderby": {"type": "string", "description": "Sort by (id, name, email, registered_date)"},
                    "order": {"type": "string", "description": "Order direction (asc, desc)"},
                },
            },
        ),
        Tool(
            name="get_customer",
            description="Get a specific customer by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Customer ID"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="create_customer",
            description="Create a new customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Customer email"},
                    "first_name": {"type": "string", "description": "First name"},
                    "last_name": {"type": "string", "description": "Last name"},
                    "username": {"type": "string", "description": "Username"},
                    "password": {"type": "string", "description": "Password"},
                    "billing": {"type": "object", "description": "Billing address"},
                    "shipping": {"type": "object", "description": "Shipping address"},
                },
                "required": ["email"],
            },
        ),
        Tool(
            name="update_customer",
            description="Update an existing customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Customer ID"},
                    "email": {"type": "string", "description": "Customer email"},
                    "first_name": {"type": "string", "description": "First name"},
                    "last_name": {"type": "string", "description": "Last name"},
                    "billing": {"type": "object", "description": "Billing address"},
                    "shipping": {"type": "object", "description": "Shipping address"},
                },
                "required": ["id"],
            },
        ),
        Tool(
            name="get_customer_downloads",
            description="Get downloads for a specific customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Customer ID"},
                },
                "required": ["id"],
            },
        ),

        # Utility tools
        Tool(
            name="health_check",
            description="Check the health status of the backend",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="test_connection",
            description="Test the connection to WooCommerce API",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution"""

    try:
        # Products tools
        if name == "list_products":
            result = await make_api_call("GET", "/products", params=arguments)
        elif name == "get_product":
            product_id = arguments.get("id")
            params = {k: v for k, v in arguments.items() if k != "id"}
            result = await make_api_call("GET", f"/products/{product_id}", params=params)
        elif name == "create_product":
            result = await make_api_call("POST", "/products", data=arguments)
        elif name == "update_product":
            product_id = arguments.pop("id")
            result = await make_api_call("PUT", f"/products/{product_id}", data=arguments)
        elif name == "delete_product":
            product_id = arguments.get("id")
            params = {k: v for k, v in arguments.items() if k != "id"}
            result = await make_api_call("DELETE", f"/products/{product_id}", params=params)

        # Categories tools
        elif name == "list_categories":
            result = await make_api_call("GET", "/categories", params=arguments)
        elif name == "get_category":
            category_id = arguments.get("id")
            result = await make_api_call("GET", f"/categories/{category_id}")
        elif name == "create_category":
            result = await make_api_call("POST", "/categories", data=arguments)
        elif name == "update_category":
            category_id = arguments.pop("id")
            result = await make_api_call("PUT", f"/categories/{category_id}", data=arguments)
        elif name == "delete_category":
            category_id = arguments.get("id")
            params = {k: v for k, v in arguments.items() if k != "id"}
            result = await make_api_call("DELETE", f"/categories/{category_id}", params=params)

        # Orders tools
        elif name == "list_orders":
            result = await make_api_call("GET", "/orders", params=arguments)
        elif name == "get_order":
            order_id = arguments.get("id")
            result = await make_api_call("GET", f"/orders/{order_id}")
        elif name == "create_order":
            result = await make_api_call("POST", "/orders", data=arguments)
        elif name == "update_order":
            order_id = arguments.pop("id")
            result = await make_api_call("PUT", f"/orders/{order_id}", data=arguments)
        elif name == "get_order_notes":
            order_id = arguments.get("id")
            result = await make_api_call("GET", f"/orders/{order_id}/notes")
        elif name == "add_order_note":
            order_id = arguments.pop("id")
            result = await make_api_call("POST", f"/orders/{order_id}/notes", data=arguments)

        # Customers tools
        elif name == "list_customers":
            result = await make_api_call("GET", "/customers", params=arguments)
        elif name == "get_customer":
            customer_id = arguments.get("id")
            result = await make_api_call("GET", f"/customers/{customer_id}")
        elif name == "create_customer":
            result = await make_api_call("POST", "/customers", data=arguments)
        elif name == "update_customer":
            customer_id = arguments.pop("id")
            result = await make_api_call("PUT", f"/customers/{customer_id}", data=arguments)
        elif name == "get_customer_downloads":
            customer_id = arguments.get("id")
            result = await make_api_call("GET", f"/customers/{customer_id}/downloads")

        # Utility tools
        elif name == "health_check":
            result = await make_api_call("GET", "/health")
        elif name == "test_connection":
            result = await make_api_call("GET", "/test")

        else:
            raise ValueError(f"Unknown tool: {name}")

        import json
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dhart-backend",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
