# MCP Server for Dhart Backend

This MCP (Model Context Protocol) server provides AI assistants with tools to interact with the Dhart WooCommerce backend API.

## Overview

The MCP server exposes a comprehensive set of tools for managing:
- **Products**: Create, read, update, delete, and list products with advanced filtering
- **Categories**: Manage product categories and hierarchies
- **Orders**: Handle order management, status updates, and notes
- **Customers**: Manage customer data and information
- **Utilities**: Health checks and API connection testing

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Configure your environment variables in `.env`:

```bash
# Backend URL where the Flask API is running
BACKEND_URL=http://localhost:5000

# WooCommerce credentials (used by the Flask backend)
WC_STORE_URL=https://your-store.com
WC_CONSUMER_KEY=your_consumer_key
WC_CONSUMER_SECRET=your_consumer_secret
```

## Usage with Claude Desktop

Add this configuration to your Claude Desktop config file:

### macOS
`~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
`%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "dhart-backend": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"],
      "env": {
        "BACKEND_URL": "http://localhost:5000"
      }
    }
  }
}
```

Replace `/absolute/path/to/mcp_server.py` with the actual path to the MCP server file.

## Usage with Other MCP Clients

Run the server directly:

```bash
python mcp_server.py
```

The server communicates via stdio (standard input/output) following the MCP protocol.

## Available Tools

### Products

#### `list_products`
List all products with optional filtering, pagination, and sorting.

**Parameters:**
- `page` (number): Page number for pagination
- `per_page` (number): Items per page (max 100)
- `search` (string): Search term
- `category` (string): Filter by category ID
- `status` (string): Filter by status (publish, draft, etc.)
- `featured` (boolean): Filter featured products
- `on_sale` (boolean): Filter products on sale
- `min_price` (string): Minimum price filter
- `max_price` (string): Maximum price filter
- `orderby` (string): Sort by (date, id, title, price)
- `order` (string): Order direction (asc, desc)
- `minimal` (boolean): Return minimal product data

**Example:**
```json
{
  "name": "list_products",
  "arguments": {
    "per_page": 10,
    "on_sale": true,
    "orderby": "price",
    "order": "asc"
  }
}
```

#### `get_product`
Get a specific product by ID.

**Parameters:**
- `id` (string, required): Product ID
- `raw` (boolean): Return raw WooCommerce data

#### `create_product`
Create a new product.

**Parameters:**
- `name` (string, required): Product name
- `type` (string, required): Product type (simple, variable, etc.)
- `regular_price` (string, required): Regular price
- `sale_price` (string): Sale price
- `description` (string): Product description
- `short_description` (string): Short description
- `categories` (array): Array of category objects with id
- `images` (array): Array of image objects with src
- `status` (string): Product status (draft, publish, etc.)

#### `update_product`
Update an existing product.

**Parameters:**
- `id` (string, required): Product ID
- Additional fields to update

#### `delete_product`
Delete a product by ID.

**Parameters:**
- `id` (string, required): Product ID
- `force` (boolean): Force permanent deletion

### Categories

#### `list_categories`
List all product categories with optional filtering.

**Parameters:**
- `page` (number): Page number
- `per_page` (number): Items per page
- `search` (string): Search term
- `parent` (string): Filter by parent category ID
- `hide_empty` (boolean): Hide empty categories
- `orderby` (string): Sort by (name, slug, count)
- `order` (string): Order direction (asc, desc)

#### `get_category`
Get a specific category by ID.

#### `create_category`
Create a new product category.

**Parameters:**
- `name` (string, required): Category name
- `slug` (string): Category slug
- `parent` (number): Parent category ID
- `description` (string): Category description
- `image` (object): Image object with src

#### `update_category`
Update an existing category.

#### `delete_category`
Delete a category by ID.

### Orders

#### `list_orders`
List all orders with optional filtering.

**Parameters:**
- `page` (number): Page number
- `per_page` (number): Items per page
- `search` (string): Search term
- `status` (string): Filter by order status
- `customer` (string): Filter by customer ID
- `product` (string): Filter by product ID
- `after` (string): Filter orders after date (ISO8601)
- `before` (string): Filter orders before date (ISO8601)

#### `get_order`
Get a specific order by ID.

#### `create_order`
Create a new order.

**Parameters:**
- `line_items` (array, required): Array of line items
- `customer_id` (number): Customer ID
- `billing` (object): Billing address object
- `shipping` (object): Shipping address object
- `payment_method` (string): Payment method ID
- `payment_method_title` (string): Payment method title
- `status` (string): Order status

**Example:**
```json
{
  "name": "create_order",
  "arguments": {
    "line_items": [
      {
        "product_id": 123,
        "quantity": 2
      }
    ],
    "billing": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com"
    }
  }
}
```

#### `update_order`
Update an existing order.

#### `get_order_notes`
Get notes for a specific order.

#### `add_order_note`
Add a note to an order.

**Parameters:**
- `id` (string, required): Order ID
- `note` (string, required): Note content
- `customer_note` (boolean): Is customer note

### Customers

#### `list_customers`
List all customers with optional filtering.

**Parameters:**
- `page` (number): Page number
- `per_page` (number): Items per page
- `search` (string): Search term
- `email` (string): Filter by email
- `role` (string): Filter by role
- `orderby` (string): Sort by (id, name, email, registered_date)
- `order` (string): Order direction (asc, desc)

#### `get_customer`
Get a specific customer by ID.

#### `create_customer`
Create a new customer.

**Parameters:**
- `email` (string, required): Customer email
- `first_name` (string): First name
- `last_name` (string): Last name
- `username` (string): Username
- `password` (string): Password
- `billing` (object): Billing address
- `shipping` (object): Shipping address

#### `update_customer`
Update an existing customer.

#### `get_customer_downloads`
Get downloads for a specific customer.

### Utilities

#### `health_check`
Check the health status of the backend.

**Example:**
```json
{
  "name": "health_check",
  "arguments": {}
}
```

#### `test_connection`
Test the connection to WooCommerce API.

## Available Resources

The MCP server also provides resources that can be read:

### `dhart://health`
Current health status of the DH Art backend.

### `dhart://config`
Configuration and environment information.

## Example Interactions

### Example 1: List Products on Sale

```
User: Show me all products that are currently on sale, sorted by price.

Assistant uses: list_products
Arguments: {
  "on_sale": true,
  "orderby": "price",
  "order": "asc",
  "per_page": 20
}
```

### Example 2: Create a New Product

```
User: Create a new product called "Artwork ABC" priced at $299.99

Assistant uses: create_product
Arguments: {
  "name": "Artwork ABC",
  "type": "simple",
  "regular_price": "299.99",
  "status": "publish"
}
```

### Example 3: Update Order Status

```
User: Mark order #1234 as completed

Assistant uses: update_order
Arguments: {
  "id": "1234",
  "status": "completed"
}
```

### Example 4: Add Order Note

```
User: Add a note to order #1234 saying "Customer requested express shipping"

Assistant uses: add_order_note
Arguments: {
  "id": "1234",
  "note": "Customer requested express shipping",
  "customer_note": false
}
```

## Architecture

The MCP server acts as a bridge between AI assistants and the Flask backend:

```
┌─────────────────┐
│   AI Assistant  │
│  (Claude, etc)  │
└────────┬────────┘
         │ MCP Protocol
         │ (stdio)
         ▼
┌─────────────────┐
│   MCP Server    │
│  (mcp_server.py)│
└────────┬────────┘
         │ HTTP/REST
         │
         ▼
┌─────────────────┐
│  Flask Backend  │
│    (app.py)     │
└────────┬────────┘
         │ WooCommerce API
         │
         ▼
┌─────────────────┐
│  WooCommerce    │
│     Store       │
└─────────────────┘
```

## Error Handling

All tools return JSON responses. In case of errors, the response will include:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "details": "Additional error details"
}
```

## Development

### Testing the MCP Server

1. Start your Flask backend:
```bash
python app.py
```

2. In another terminal, test the MCP server:
```bash
python mcp_server.py
```

### Adding New Tools

To add a new tool:

1. Add the tool definition in `handle_list_tools()`
2. Add the tool handler in `handle_call_tool()`
3. Update this documentation

## Troubleshooting

### MCP Server Not Connecting

- Ensure the Flask backend is running and accessible at `BACKEND_URL`
- Check that the `BACKEND_URL` environment variable is set correctly
- Verify the backend is healthy: `curl http://localhost:5000/health`

### Tools Returning Errors

- Check the Flask backend logs for error details
- Verify WooCommerce API credentials are correct
- Ensure the WooCommerce store is accessible

### Claude Desktop Not Finding Server

- Verify the absolute path in `claude_desktop_config.json` is correct
- Restart Claude Desktop after configuration changes
- Check Claude Desktop logs for connection errors

## Security Notes

- The MCP server communicates with the Flask backend, which securely handles WooCommerce credentials
- Never expose WooCommerce credentials in the MCP server configuration
- Always use HTTPS in production for the Flask backend
- Consider implementing authentication between MCP server and Flask backend for production use

## License

This MCP server is part of the DH Art Backend project.

## Support

For issues or questions:
1. Check the main backend documentation
2. Review the troubleshooting section above
3. Check Flask backend logs for detailed error information
