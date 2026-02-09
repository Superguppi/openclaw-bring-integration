# Bring! Shopping List - OpenClaw Skill

## Overview

This skill enables OpenClaw to interact with Bring! Shopping Lists (getbring.com), allowing the agent to manage shopping lists for users.

## Capabilities

- 📋 **List Management**: View all shopping lists
- 🔍 **Browse Items**: See what's on a shopping list
- ➕ **Add Items**: Add single or multiple items to lists
- ✅ **Complete Items**: Mark items as purchased
- 🗑️ **Remove Items**: Remove items from lists
- 📊 **Summaries**: Get formatted list overviews

## Configuration

### Environment Variables

```bash
BRING_EMAIL=your-email@example.com
BRING_PASSWORD=your-password
```

Or create a `.env` file in the skill directory.

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure credentials (see above)

3. Test the connection:
   ```bash
   python bring_client.py
   ```

## Usage in OpenClaw

### Import the Integration

```python
from bring_integration import BringIntegration

# Initialize
async with BringIntegration() as bring:
    # Use the integration
    lists = await bring.get_lists()
```

### Common Operations

#### Get All Lists

```python
lists = await bring.get_lists()
# Returns: [{"listUuid": "...", "name": "Weekly Shopping", ...}]
```

#### Set Default List

```python
await bring.set_default_list("Weekly Shopping")
# Now operations can omit list_name parameter
```

#### Add Items

```python
# Single item
await bring.add_item("Milk", specification="1 liter")

# With list name
await bring.add_item("Bread", list_name="Weekly Shopping")

# Multiple items
await bring.add_items(["Eggs", "Cheese", "Butter"])
```

#### View List Contents

```python
items = await bring.get_items("Weekly Shopping")
# Returns: {"purchase": [...], "recently": [...]}

# Or get formatted summary
summary = await bring.format_list_summary("Weekly Shopping")
print(summary)
```

#### Complete Items

```python
await bring.complete_item("Milk")
```

#### Remove Items

```python
await bring.remove_item("Old Item")
```

## Agent Examples

### Example 1: Natural Language Shopping List

```
User: "Add milk and bread to my shopping list"

Agent workflow:
1. Initialize BringIntegration
2. Get user's lists (or use default)
3. Call bring.add_items(["Milk", "Bread"])
4. Respond: "Added Milk and Bread to your shopping list ✅"
```

### Example 2: List Overview

```
User: "What's on my shopping list?"

Agent workflow:
1. Initialize BringIntegration
2. Call bring.format_list_summary()
3. Send formatted response to user
```

### Example 3: Mark Items Complete

```
User: "I bought the milk"

Agent workflow:
1. Initialize BringIntegration
2. Call bring.complete_item("Milk")
3. Respond: "Marked Milk as purchased ✅"
```

## Tool Functions

For OpenClaw tool integration, expose these functions:

### `bring_get_lists()`

Returns all shopping lists.

**Returns**: `List[Dict]` - List metadata

### `bring_show_list(list_name: str)`

Show items on a shopping list.

**Args**:
- `list_name`: Name of the list

**Returns**: `str` - Formatted list summary

### `bring_add_item(item_name: str, specification: str = "", list_name: str = None)`

Add an item to a shopping list.

**Args**:
- `item_name`: Name of the item
- `specification`: Optional details (e.g., "2 kg")
- `list_name`: Optional list name (uses default if not provided)

**Returns**: `bool` - Success status

### `bring_add_items(items: List[str], list_name: str = None)`

Add multiple items at once.

**Args**:
- `items`: List of item names
- `list_name`: Optional list name

**Returns**: `bool` - Success status

### `bring_complete_item(item_name: str, list_name: str = None)`

Mark an item as purchased.

**Args**:
- `item_name`: Name of the item
- `list_name`: Optional list name

**Returns**: `bool` - Success status

### `bring_remove_item(item_name: str, list_name: str = None)`

Remove an item from the list.

**Args**:
- `item_name`: Name of the item
- `list_name`: Optional list name

**Returns**: `bool` - Success status

## Error Handling

The integration handles common errors:

- **Authentication failures**: Invalid credentials
- **List not found**: Invalid list name
- **Connection errors**: Network issues
- **API rate limiting**: Too many requests

Always use try-except blocks:

```python
try:
    await bring.add_item("Milk")
except ValueError as e:
    # List not found or credentials missing
    print(f"Configuration error: {e}")
except Exception as e:
    # Network or API error
    print(f"Operation failed: {e}")
```

## Notes

- Uses unofficial Bring! API (may change)
- Requires active internet connection
- List names are case-insensitive
- Items are identified by name (not UUID) for simplicity
- Supports multiple lists per account
- Recently completed items are shown separately

## API Reference

Based on [`bring-api`](https://github.com/miaucl/bring-api) library.

**Key Endpoints**:
- Login & authentication
- Load lists
- Get list items
- Save/update items
- Complete items
- Remove items
- Batch operations

## Dependencies

- `bring-api>=6.0.0` - Unofficial Bring! API client
- `aiohttp>=3.8.0` - Async HTTP client
- `python-dotenv>=1.0.0` - Environment variable management

## License

MIT License - See original `bring-api` project

## Disclaimer

Not affiliated with Bring! Labs AG. Unofficial integration using reverse-engineered API.
