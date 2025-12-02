"""
Inventory Routes
Defines API endpoints for inventory and product management
"""
from fastapi import APIRouter, Depends
from typing import Dict

from ..controllers.inventory_controller import InventoryController

router = APIRouter(prefix="", tags=["Inventory"])


def get_dependencies():
    """Dependency injection for engine"""
    from ..config.database import get_engine
    return {"engine": get_engine()}


@router.get("/ingredients")
def get_ingredients(deps: Dict = Depends(get_dependencies)):
    """
    Get all ingredients with their stock levels
    """
    return InventoryController.get_ingredients(deps["engine"])


@router.post("/ingredients")
def create_ingredient(ingredient: dict, deps: Dict = Depends(get_dependencies)):
    """
    Create a new ingredient
    """
    return InventoryController.create_ingredient(deps["engine"], ingredient)


@router.put("/ingredients/{ingredient_id}")
def update_ingredient(ingredient_id: int, ingredient: dict, deps: Dict = Depends(get_dependencies)):
    """
    Update an existing ingredient
    """
    return InventoryController.update_ingredient(deps["engine"], ingredient_id, ingredient)


@router.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, deps: Dict = Depends(get_dependencies)):
    """
    Delete an ingredient
    """
    return InventoryController.delete_ingredient(deps["engine"], ingredient_id)


@router.get("/products")
def get_products(deps: Dict = Depends(get_dependencies)):
    """
    Get all products (coffee items)
    """
    return InventoryController.get_products(deps["engine"])


@router.get("/products/{product_id}/cost-analysis")
def get_product_cost_analysis(product_id: int, deps: Dict = Depends(get_dependencies)):
    """
    Calculate the cost breakdown and profit margin for a product
    """
    return InventoryController.get_product_cost_analysis(deps["engine"], product_id)
