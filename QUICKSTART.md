# Quick Start Guide

Get started with the OpenClaw Bring! Integration in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install bring-api aiohttp python-dotenv
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## Step 2: Configure Credentials

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Bring! credentials:

```
BRING_EMAIL=your-email@example.com
BRING_PASSWORD=your-password
```

## Step 3: Test the Connection

Run the basic client test:

```bash
python bring_client.py
```

You should see your shopping lists and their items!

## Step 4: Try the CLI

```bash
# See all your lists
python bring_cli.py lists

# Show items on a list (replace with your list name)
python bring_cli.py show "My Shopping List"

# Add an item
python bring_cli.py add "My Shopping List" "Milk" --spec "1 liter"

# Mark as complete
python bring_cli.py complete "My Shopping List" "Milk"
```

## Step 5: Use in Python

```python
import asyncio
from bring_integration import BringIntegration

async def main():
    async with BringIntegration() as bring:
        # Get your lists
        lists = await bring.get_lists()
        print(f"Found {len(lists)} lists")
        
        # Set a default list
        await bring.set_default_list(lists[0]['name'])
        
        # Add items
        await bring.add_item("Coffee", "250g")
        await bring.add_items(["Milk", "Bread", "Eggs"])
        
        # Show the list
        summary = await bring.format_list_summary()
        print(summary)

asyncio.run(main())
```

## Step 6: Run Examples

```bash
python example_usage.py
```

This will show you various usage patterns!

## Common Issues

### "No credentials found"

Make sure your `.env` file exists and contains valid credentials.

### "Event loop is closed" (Windows)

Add this at the start of your script:

```python
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

### "Authentication failed"

- Check your email and password
- Bring! doesn't support 2FA with this API
- Make sure your account is activated

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [SKILL.md](SKILL.md) for OpenClaw integration details
- See [example_usage.py](example_usage.py) for more patterns
- Look at [bring_cli.py](bring_cli.py) for CLI usage

## Need Help?

Open an issue on GitHub or check the documentation!

Happy shopping! 🛒✨
