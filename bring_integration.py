"""
OpenClaw Bring! Integration
Main integration module for using Bring! with OpenClaw
"""

import os
import logging
from typing import List, Dict, Optional, Any
from bring_client import BringClient

logger = logging.getLogger(__name__)


class BringIntegration:
    """
    OpenClaw integration for Bring! Shopping Lists
    
    This class provides a high-level interface for OpenClaw agents to interact
    with Bring! shopping lists.
    """
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the Bring! integration
        
        Args:
            email: Bring! account email (or set BRING_EMAIL env var)
            password: Bring! account password (or set BRING_PASSWORD env var)
        """
        self.email = email or os.getenv("BRING_EMAIL")
        self.password = password or os.getenv("BRING_PASSWORD")
        
        if not self.email or not self.password:
            raise ValueError(
                "Bring! credentials not provided. "
                "Set BRING_EMAIL and BRING_PASSWORD environment variables "
                "or pass them to the constructor."
            )
            
        self.client: Optional[BringClient] = None
        self._default_list_uuid: Optional[str] = None
        
    async def initialize(self):
        """Initialize and connect to Bring! API"""
        if self.client is None:
            self.client = BringClient(self.email, self.password)
            await self.client.connect()
            logger.info("Bring! integration initialized")
            
    async def cleanup(self):
        """Cleanup and disconnect"""
        if self.client:
            await self.client.disconnect()
            self.client = None
            
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()
        
    # ==================== List Operations ====================
    
    async def get_lists(self) -> List[Dict[str, Any]]:
        """
        Get all shopping lists
        
        Returns:
            List of shopping lists with metadata
            
        Example:
            [
                {
                    "listUuid": "abc-123",
                    "name": "Weekly Shopping",
                    "theme": "ch.publisheria.bring.theme.purple"
                }
            ]
        """
        await self.initialize()
        return await self.client.get_lists()
        
    async def find_list(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find a list by name (case-insensitive)
        
        Args:
            name: Name of the list to find
            
        Returns:
            List metadata or None if not found
        """
        await self.initialize()
        return await self.client.get_list_by_name(name)
        
    async def set_default_list(self, name: str) -> bool:
        """
        Set a default list for operations that don't specify a list
        
        Args:
            name: Name of the list
            
        Returns:
            True if list was found and set
        """
        lst = await self.find_list(name)
        if lst:
            self._default_list_uuid = lst['listUuid']
            logger.info(f"Default list set to '{name}' ({self._default_list_uuid})")
            return True
        return False
        
    def _get_list_uuid(self, list_name: Optional[str] = None) -> str:
        """
        Helper to get list UUID from name or use default
        
        Args:
            list_name: Optional list name
            
        Returns:
            List UUID
            
        Raises:
            ValueError: If no list specified and no default set
        """
        if list_name:
            # Will be resolved in async context
            return list_name
        elif self._default_list_uuid:
            return self._default_list_uuid
        else:
            raise ValueError(
                "No list specified and no default list set. "
                "Use set_default_list() or provide list_name parameter."
            )
    
    # ==================== Item Operations ====================
    
    async def get_items(
        self, 
        list_name: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get items from a shopping list
        
        Args:
            list_name: Name of the list (or use default)
            
        Returns:
            Dictionary with 'purchase' and 'recently' lists
            
        Example:
            {
                "purchase": [
                    {"name": "Milk", "specification": "1 liter"},
                    {"name": "Bread", "specification": ""}
                ],
                "recently": [
                    {"name": "Eggs", "specification": "6 pieces"}
                ]
            }
        """
        await self.initialize()
        
        # Resolve list UUID
        if list_name:
            lst = await self.find_list(list_name)
            if not lst:
                raise ValueError(f"List '{list_name}' not found")
            list_uuid = lst['listUuid']
        else:
            list_uuid = self._get_list_uuid()
            
        return await self.client.get_items(list_uuid)
        
    async def add_item(
        self,
        item_name: str,
        specification: str = "",
        list_name: Optional[str] = None
    ) -> bool:
        """
        Add an item to a shopping list
        
        Args:
            item_name: Name of the item
            specification: Optional details (e.g., "2 kg", "organic")
            list_name: Name of the list (or use default)
            
        Returns:
            True if successful
        """
        await self.initialize()
        
        if list_name:
            lst = await self.find_list(list_name)
            if not lst:
                raise ValueError(f"List '{list_name}' not found")
            list_uuid = lst['listUuid']
        else:
            list_uuid = self._get_list_uuid()
            
        return await self.client.add_item(list_uuid, item_name, specification)
        
    async def add_items(
        self,
        items: List[str],
        list_name: Optional[str] = None
    ) -> bool:
        """
        Add multiple items to a shopping list
        
        Args:
            items: List of item names (strings) or dicts with 'name' and 'spec'
            list_name: Name of the list (or use default)
            
        Returns:
            True if successful
        """
        await self.initialize()
        
        if list_name:
            lst = await self.find_list(list_name)
            if not lst:
                raise ValueError(f"List '{list_name}' not found")
            list_uuid = lst['listUuid']
        else:
            list_uuid = self._get_list_uuid()
            
        # Convert items to proper format
        formatted_items = []
        for item in items:
            if isinstance(item, str):
                formatted_items.append({"itemId": item})
            elif isinstance(item, dict):
                formatted_items.append({
                    "itemId": item.get("name", item.get("itemId")),
                    "spec": item.get("spec", item.get("specification", ""))
                })
                
        return await self.client.batch_add_items(list_uuid, formatted_items)
        
    async def complete_item(
        self,
        item_name: str,
        list_name: Optional[str] = None
    ) -> bool:
        """
        Mark an item as completed
        
        Args:
            item_name: Name of the item
            list_name: Name of the list (or use default)
            
        Returns:
            True if successful
        """
        await self.initialize()
        
        if list_name:
            lst = await self.find_list(list_name)
            if not lst:
                raise ValueError(f"List '{list_name}' not found")
            list_uuid = lst['listUuid']
        else:
            list_uuid = self._get_list_uuid()
            
        return await self.client.complete_item(list_uuid, item_name)
        
    async def remove_item(
        self,
        item_name: str,
        list_name: Optional[str] = None
    ) -> bool:
        """
        Remove an item from a shopping list
        
        Args:
            item_name: Name of the item
            list_name: Name of the list (or use default)
            
        Returns:
            True if successful
        """
        await self.initialize()
        
        if list_name:
            lst = await self.find_list(list_name)
            if not lst:
                raise ValueError(f"List '{list_name}' not found")
            list_uuid = lst['listUuid']
        else:
            list_uuid = self._get_list_uuid()
            
        return await self.client.remove_item(list_uuid, item_name)
        
    # ==================== Utility Methods ====================
    
    async def format_list_summary(self, list_name: Optional[str] = None) -> str:
        """
        Get a formatted text summary of a shopping list
        
        Args:
            list_name: Name of the list (or use default)
            
        Returns:
            Formatted string with list contents
        """
        items = await self.get_items(list_name)
        
        # Get list name
        if list_name:
            lst = await self.find_list(list_name)
            display_name = lst['name'] if lst else "Shopping List"
        else:
            lists = await self.get_lists()
            for lst in lists:
                if lst['listUuid'] == self._default_list_uuid:
                    display_name = lst['name']
                    break
            else:
                display_name = "Shopping List"
                
        lines = [f"📋 {display_name}\n"]
        
        # To buy
        purchase = items.get('purchase', [])
        if purchase:
            lines.append("🛒 To Buy:")
            for item in purchase:
                spec = f" ({item['specification']})" if item.get('specification') else ""
                lines.append(f"  ☐ {item['name']}{spec}")
        else:
            lines.append("🛒 To Buy: (empty)")
            
        # Recently purchased
        recently = items.get('recently', [])
        if recently:
            lines.append("\n✅ Recently Purchased:")
            for item in recently[:5]:  # Show only last 5
                spec = f" ({item['specification']})" if item.get('specification') else ""
                lines.append(f"  ✓ {item['name']}{spec}")
                
        return "\n".join(lines)


# Example usage
async def demo():
    """Demo of the integration"""
    import asyncio
    from dotenv import load_dotenv
    
    load_dotenv()
    
    async with BringIntegration() as bring:
        # Get all lists
        lists = await bring.get_lists()
        print(f"Found {len(lists)} lists")
        
        if lists:
            # Set default list
            await bring.set_default_list(lists[0]['name'])
            
            # Add some items
            await bring.add_item("Milk", "1 liter")
            await bring.add_item("Bread")
            await bring.add_items(["Eggs", "Cheese", "Butter"])
            
            # Show list
            summary = await bring.format_list_summary()
            print("\n" + summary)
            
            # Complete an item
            await bring.complete_item("Milk")
            
            # Show updated list
            summary = await bring.format_list_summary()
            print("\n" + summary)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import asyncio
    asyncio.run(demo())
