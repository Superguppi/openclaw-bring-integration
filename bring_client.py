"""
Bring! API Client
Wrapper around the bring-api library for easier use in OpenClaw
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional, Any
from bring_api import Bring, BringItemOperation
import logging

logger = logging.getLogger(__name__)


class BringClient:
    """
    Client for interacting with the Bring! Shopping List API
    """
    
    def __init__(self, email: str, password: str):
        """
        Initialize the Bring! client
        
        Args:
            email: Bring! account email
            password: Bring! account password
        """
        self.email = email
        self.password = password
        self.session: Optional[aiohttp.ClientSession] = None
        self.bring: Optional[Bring] = None
        self._lists_cache: Optional[List[Dict]] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
        
    async def connect(self):
        """Establish connection and login to Bring!"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self.bring = Bring(self.session, self.email, self.password)
            await self.bring.login()
            logger.info("Successfully connected to Bring! API")
            
    async def disconnect(self):
        """Close the connection"""
        if self.session:
            await self.session.close()
            self.session = None
            self.bring = None
            logger.info("Disconnected from Bring! API")
            
    async def get_lists(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get all shopping lists
        
        Args:
            force_refresh: Force refresh the cache
            
        Returns:
            List of shopping lists with their metadata
        """
        if not self.bring:
            await self.connect()
            
        if self._lists_cache is None or force_refresh:
            response = await self.bring.load_lists()
            self._lists_cache = response.get("lists", [])
            logger.debug(f"Loaded {len(self._lists_cache)} lists")
            
        return self._lists_cache
        
    async def get_list_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a list by its name
        
        Args:
            name: Name of the list
            
        Returns:
            List metadata or None if not found
        """
        lists = await self.get_lists()
        for lst in lists:
            if lst.get("name", "").lower() == name.lower():
                return lst
        return None
        
    async def get_items(self, list_uuid: str) -> Dict[str, Any]:
        """
        Get all items from a shopping list
        
        Args:
            list_uuid: UUID of the shopping list
            
        Returns:
            Dictionary with 'purchase' (items to buy) and 'recently' (completed items)
        """
        if not self.bring:
            await self.connect()
            
        items = await self.bring.get_list(list_uuid)
        logger.debug(f"Retrieved {len(items.get('purchase', []))} items from list {list_uuid}")
        return items
        
    async def add_item(
        self, 
        list_uuid: str, 
        item_name: str, 
        specification: str = ""
    ) -> bool:
        """
        Add an item to a shopping list
        
        Args:
            list_uuid: UUID of the shopping list
            item_name: Name of the item
            specification: Optional specification (e.g., "2 kg", "low fat")
            
        Returns:
            True if successful
        """
        if not self.bring:
            await self.connect()
            
        await self.bring.save_item(list_uuid, item_name, specification)
        logger.info(f"Added '{item_name}' to list {list_uuid}")
        return True
        
    async def complete_item(self, list_uuid: str, item_name: str) -> bool:
        """
        Mark an item as completed
        
        Args:
            list_uuid: UUID of the shopping list
            item_name: Name of the item
            
        Returns:
            True if successful
        """
        if not self.bring:
            await self.connect()
            
        await self.bring.complete_item(list_uuid, item_name)
        logger.info(f"Completed '{item_name}' on list {list_uuid}")
        return True
        
    async def remove_item(self, list_uuid: str, item_name: str) -> bool:
        """
        Remove an item from a shopping list
        
        Args:
            list_uuid: UUID of the shopping list
            item_name: Name of the item
            
        Returns:
            True if successful
        """
        if not self.bring:
            await self.connect()
            
        await self.bring.remove_item(list_uuid, item_name)
        logger.info(f"Removed '{item_name}' from list {list_uuid}")
        return True
        
    async def batch_add_items(
        self, 
        list_uuid: str, 
        items: List[Dict[str, str]]
    ) -> bool:
        """
        Add multiple items at once
        
        Args:
            list_uuid: UUID of the shopping list
            items: List of items, each with 'itemId' and optional 'spec'
            
        Returns:
            True if successful
        """
        if not self.bring:
            await self.connect()
            
        await self.bring.batch_update_list(
            list_uuid,
            items,
            BringItemOperation.ADD
        )
        logger.info(f"Batch added {len(items)} items to list {list_uuid}")
        return True
        
    async def get_user_info(self) -> Dict[str, Any]:
        """
        Get user account information
        
        Returns:
            User information dictionary
        """
        if not self.bring:
            await self.connect()
            
        # Note: This might need to be implemented if the API supports it
        # For now, return basic info
        lists = await self.get_lists()
        return {
            "email": self.email,
            "list_count": len(lists)
        }


# Example usage
async def main():
    """Example usage of the BringClient"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    email = os.getenv("BRING_EMAIL")
    password = os.getenv("BRING_PASSWORD")
    
    if not email or not password:
        print("Please set BRING_EMAIL and BRING_PASSWORD in .env file")
        return
        
    async with BringClient(email, password) as client:
        # Get all lists
        lists = await client.get_lists()
        print(f"\nYour shopping lists ({len(lists)}):")
        for lst in lists:
            print(f"  - {lst['name']} (UUID: {lst['listUuid']})")
            
        if lists:
            # Get items from first list
            list_uuid = lists[0]['listUuid']
            items = await client.get_items(list_uuid)
            
            print(f"\nItems on '{lists[0]['name']}':")
            for item in items.get('purchase', []):
                spec = f" ({item['specification']})" if item.get('specification') else ""
                print(f"  ☐ {item['name']}{spec}")
                
            print(f"\nRecently purchased:")
            for item in items.get('recently', []):
                spec = f" ({item['specification']})" if item.get('specification') else ""
                print(f"  ✓ {item['name']}{spec}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
