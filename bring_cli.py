#!/usr/bin/env python3
"""
Bring! CLI Tool
Command-line interface for managing Bring! shopping lists
"""

import asyncio
import sys
import argparse
import logging
from typing import Optional
from dotenv import load_dotenv
from bring_integration import BringIntegration


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


async def cmd_lists(bring: BringIntegration):
    """List all shopping lists"""
    lists = await bring.get_lists()
    
    if not lists:
        print("No shopping lists found.")
        return
        
    print(f"\n📋 Your Shopping Lists ({len(lists)}):\n")
    for i, lst in enumerate(lists, 1):
        print(f"{i}. {lst['name']}")
        print(f"   UUID: {lst['listUuid']}")
        print(f"   Theme: {lst.get('theme', 'default')}")
        print()


async def cmd_show(bring: BringIntegration, list_name: str):
    """Show items on a shopping list"""
    summary = await bring.format_list_summary(list_name)
    print("\n" + summary + "\n")


async def cmd_add(
    bring: BringIntegration,
    list_name: str,
    item_name: str,
    specification: Optional[str] = None
):
    """Add an item to a shopping list"""
    spec = specification or ""
    success = await bring.add_item(item_name, spec, list_name)
    
    if success:
        spec_str = f" ({spec})" if spec else ""
        print(f"✅ Added '{item_name}{spec_str}' to '{list_name}'")
    else:
        print(f"❌ Failed to add item")
        sys.exit(1)


async def cmd_complete(bring: BringIntegration, list_name: str, item_name: str):
    """Mark an item as completed"""
    success = await bring.complete_item(item_name, list_name)
    
    if success:
        print(f"✅ Marked '{item_name}' as completed")
    else:
        print(f"❌ Failed to complete item")
        sys.exit(1)


async def cmd_remove(bring: BringIntegration, list_name: str, item_name: str):
    """Remove an item from a shopping list"""
    success = await bring.remove_item(item_name, list_name)
    
    if success:
        print(f"🗑️  Removed '{item_name}' from '{list_name}'")
    else:
        print(f"❌ Failed to remove item")
        sys.exit(1)


async def cmd_batch_add(bring: BringIntegration, list_name: str, items: list):
    """Add multiple items at once"""
    success = await bring.add_items(items, list_name)
    
    if success:
        print(f"✅ Added {len(items)} items to '{list_name}':")
        for item in items:
            print(f"  - {item}")
    else:
        print(f"❌ Failed to add items")
        sys.exit(1)


async def main():
    """Main CLI entry point"""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description="Bring! Shopping List CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s lists                                 # Show all lists
  %(prog)s show "Weekly Shopping"                # Show items on a list
  %(prog)s add "Weekly Shopping" "Milk"          # Add an item
  %(prog)s add "Weekly Shopping" "Milk" --spec "1 liter"  # Add with specification
  %(prog)s complete "Weekly Shopping" "Milk"     # Mark as completed
  %(prog)s remove "Weekly Shopping" "Milk"       # Remove an item
  %(prog)s batch "Weekly Shopping" Milk Bread Eggs  # Add multiple items
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Lists command
    subparsers.add_parser('lists', help='List all shopping lists')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show items on a list')
    show_parser.add_argument('list_name', help='Name of the list')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add an item to a list')
    add_parser.add_argument('list_name', help='Name of the list')
    add_parser.add_argument('item_name', help='Name of the item')
    add_parser.add_argument('--spec', '--specification', dest='specification',
                           help='Item specification (e.g., "2 kg", "organic")')
    
    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark an item as completed')
    complete_parser.add_argument('list_name', help='Name of the list')
    complete_parser.add_argument('item_name', help='Name of the item')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove an item')
    remove_parser.add_argument('list_name', help='Name of the list')
    remove_parser.add_argument('item_name', help='Name of the item')
    
    # Batch add command
    batch_parser = subparsers.add_parser('batch', help='Add multiple items at once')
    batch_parser.add_argument('list_name', help='Name of the list')
    batch_parser.add_argument('items', nargs='+', help='Items to add')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    setup_logging(args.verbose)
    
    try:
        async with BringIntegration() as bring:
            if args.command == 'lists':
                await cmd_lists(bring)
                
            elif args.command == 'show':
                await cmd_show(bring, args.list_name)
                
            elif args.command == 'add':
                await cmd_add(bring, args.list_name, args.item_name, args.specification)
                
            elif args.command == 'complete':
                await cmd_complete(bring, args.list_name, args.item_name)
                
            elif args.command == 'remove':
                await cmd_remove(bring, args.list_name, args.item_name)
                
            elif args.command == 'batch':
                await cmd_batch_add(bring, args.list_name, args.items)
                
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
