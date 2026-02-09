#!/usr/bin/env python3
"""
Example usage of the Bring! Integration for OpenClaw
This demonstrates various use cases and patterns
"""

import asyncio
import logging
from dotenv import load_dotenv
from bring_integration import BringIntegration


async def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    async with BringIntegration() as bring:
        # Get all lists
        lists = await bring.get_lists()
        print(f"\nYou have {len(lists)} shopping list(s):")
        for lst in lists:
            print(f"  - {lst['name']}")
            
        if lists:
            # Work with the first list
            list_name = lists[0]['name']
            print(f"\nWorking with list: '{list_name}'")
            
            # Add an item
            await bring.add_item("Example Item", "from Python", list_name)
            print("✅ Added example item")
            
            # Show the list
            summary = await bring.format_list_summary(list_name)
            print(f"\n{summary}")


async def example_default_list():
    """Using a default list"""
    print("\n" + "=" * 60)
    print("Example 2: Using Default List")
    print("=" * 60)
    
    async with BringIntegration() as bring:
        lists = await bring.get_lists()
        
        if not lists:
            print("No lists found!")
            return
            
        # Set default list
        list_name = lists[0]['name']
        await bring.set_default_list(list_name)
        print(f"\n✅ Set '{list_name}' as default list")
        
        # Now we can omit list_name in operations
        await bring.add_item("Milk", "1 liter")
        await bring.add_item("Bread")
        print("✅ Added items to default list")
        
        # Show the list
        summary = await bring.format_list_summary()
        print(f"\n{summary}")


async def example_batch_operations():
    """Batch adding items"""
    print("\n" + "=" * 60)
    print("Example 3: Batch Operations")
    print("=" * 60)
    
    async with BringIntegration() as bring:
        lists = await bring.get_lists()
        
        if not lists:
            print("No lists found!")
            return
            
        list_name = lists[0]['name']
        
        # Add multiple items at once
        shopping_items = [
            "Eggs",
            "Cheese",
            "Butter",
            "Tomatoes",
            "Onions"
        ]
        
        await bring.add_items(shopping_items, list_name)
        print(f"✅ Added {len(shopping_items)} items in one go")
        
        # Show the list
        summary = await bring.format_list_summary(list_name)
        print(f"\n{summary}")


async def example_complete_and_remove():
    """Completing and removing items"""
    print("\n" + "=" * 60)
    print("Example 4: Complete and Remove Items")
    print("=" * 60)
    
    async with BringIntegration() as bring:
        lists = await bring.get_lists()
        
        if not lists:
            print("No lists found!")
            return
            
        list_name = lists[0]['name']
        await bring.set_default_list(list_name)
        
        # Add a test item
        await bring.add_item("Test Item", "to be completed")
        print("✅ Added test item")
        
        # Show list before
        print("\nBefore completing:")
        items = await bring.get_items()
        print(f"  To buy: {len(items['purchase'])} items")
        print(f"  Recently: {len(items['recently'])} items")
        
        # Complete the item
        await bring.complete_item("Test Item")
        print("\n✅ Completed test item")
        
        # Show list after
        print("\nAfter completing:")
        items = await bring.get_items()
        print(f"  To buy: {len(items['purchase'])} items")
        print(f"  Recently: {len(items['recently'])} items")
        
        # Remove the item
        await bring.remove_item("Test Item")
        print("\n🗑️  Removed test item")


async def example_conversational():
    """Simulating a conversational agent interaction"""
    print("\n" + "=" * 60)
    print("Example 5: Conversational Agent Pattern")
    print("=" * 60)
    
    async def agent_response(user_message: str, bring: BringIntegration):
        """Simulate agent processing user messages"""
        print(f"\n👤 User: {user_message}")
        
        msg_lower = user_message.lower()
        
        # Parse intent
        if "add" in msg_lower:
            # Extract items (very simple parsing)
            if "milk" in msg_lower:
                await bring.add_item("Milk")
                print("🤖 Agent: Added Milk to your shopping list ✅")
            if "bread" in msg_lower:
                await bring.add_item("Bread")
                print("🤖 Agent: Added Bread to your shopping list ✅")
                
        elif "show" in msg_lower or "what" in msg_lower:
            summary = await bring.format_list_summary()
            print(f"🤖 Agent:\n{summary}")
            
        elif "bought" in msg_lower or "got" in msg_lower:
            if "milk" in msg_lower:
                await bring.complete_item("Milk")
                print("🤖 Agent: Marked Milk as purchased ✅")
                
        else:
            print("🤖 Agent: I can help you manage your shopping list!")
    
    # Simulate conversation
    async with BringIntegration() as bring:
        lists = await bring.get_lists()
        if lists:
            await bring.set_default_list(lists[0]['name'])
            
            # Simulated user messages
            await agent_response("Add milk and bread to my list", bring)
            await agent_response("What's on my shopping list?", bring)
            await agent_response("I bought the milk", bring)
            await agent_response("Show me my list", bring)


async def example_error_handling():
    """Demonstrating error handling"""
    print("\n" + "=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)
    
    async with BringIntegration() as bring:
        # Try to add to non-existent list
        try:
            await bring.add_item("Test", list_name="NonExistentList")
        except ValueError as e:
            print(f"✅ Caught expected error: {e}")
            
        # Try to use default list without setting it
        try:
            bring._default_list_uuid = None  # Reset default
            await bring.add_item("Test")
        except ValueError as e:
            print(f"✅ Caught expected error: {e}")


async def main():
    """Run all examples"""
    load_dotenv()
    
    print("\n" + "=" * 60)
    print("Bring! Integration - Usage Examples")
    print("=" * 60)
    
    try:
        await example_basic_usage()
        await example_default_list()
        await example_batch_operations()
        await example_complete_and_remove()
        await example_conversational()
        await example_error_handling()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully! ✅")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,  # Less verbose for examples
        format='%(levelname)s: %(message)s'
    )
    
    asyncio.run(main())
