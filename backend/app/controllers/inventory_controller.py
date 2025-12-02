"""
Inventory Controller
Handles HTTP requests for inventory and product endpoints
"""
import pandas as pd
from fastapi import HTTPException
from sqlalchemy import text
from typing import Dict


class InventoryController:
    """Controller for inventory and product endpoints"""

    @staticmethod
    def get_ingredients(engine) -> Dict:
        """Get all ingredients"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            query = """
                SELECT
                    id, name, unit, stock_quantity, reorder_level,
                    unit_cost, supplier, notes, created_at, updated_at
                FROM ingredients
                ORDER BY name
            """

            df = pd.read_sql(query, engine)

            if df.empty:
                return {"ingredients": []}

            ingredients = df.to_dict('records')

            for ingredient in ingredients:
                ingredient['stock_quantity'] = float(ingredient['stock_quantity'])
                ingredient['reorder_level'] = float(ingredient['reorder_level'])
                ingredient['unit_cost'] = float(ingredient['unit_cost']) if ingredient['unit_cost'] else 0
                ingredient['created_at'] = ingredient['created_at'].isoformat() if ingredient['created_at'] else None
                ingredient['updated_at'] = ingredient['updated_at'].isoformat() if ingredient['updated_at'] else None
                ingredient['is_low_stock'] = ingredient['stock_quantity'] < ingredient['reorder_level']

            return {"ingredients": ingredients}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ingredients: {str(e)}")

    @staticmethod
    def create_ingredient(engine, ingredient: dict) -> Dict:
        """Create a new ingredient"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            required_fields = ['name', 'unit', 'stock_quantity', 'reorder_level']
            for field in required_fields:
                if field not in ingredient:
                    raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

            query = """
                INSERT INTO ingredients (name, unit, stock_quantity, reorder_level, unit_cost, supplier, notes)
                VALUES (:name, :unit, :stock_quantity, :reorder_level, :unit_cost, :supplier, :notes)
            """

            params = {
                'name': ingredient['name'],
                'unit': ingredient['unit'],
                'stock_quantity': ingredient['stock_quantity'],
                'reorder_level': ingredient['reorder_level'],
                'unit_cost': ingredient.get('unit_cost', 0),
                'supplier': ingredient.get('supplier', ''),
                'notes': ingredient.get('notes', '')
            }

            with engine.begin() as conn:
                result = conn.execute(text(query), params)
                try:
                    ingredient_id = result.lastrowid
                except Exception:
                    ingredient_id = conn.execute(text("SELECT LAST_INSERT_ID() AS id")).scalar()

            return {"message": "Ingredient created successfully", "id": ingredient_id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating ingredient: {str(e)}")

    @staticmethod
    def update_ingredient(engine, ingredient_id: int, ingredient: dict) -> Dict:
        """Update an existing ingredient"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            query = """
                UPDATE ingredients
                SET name = :name, unit = :unit, stock_quantity = :stock_quantity,
                    reorder_level = :reorder_level, unit_cost = :unit_cost,
                    supplier = :supplier, notes = :notes
                WHERE id = :id
            """

            params = {
                'id': ingredient_id,
                'name': ingredient['name'],
                'unit': ingredient['unit'],
                'stock_quantity': ingredient['stock_quantity'],
                'reorder_level': ingredient['reorder_level'],
                'unit_cost': ingredient.get('unit_cost', 0),
                'supplier': ingredient.get('supplier', ''),
                'notes': ingredient.get('notes', '')
            }

            with engine.begin() as conn:
                conn.execute(text(query), params)

            return {"message": "Ingredient updated successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating ingredient: {str(e)}")

    @staticmethod
    def delete_ingredient(engine, ingredient_id: int) -> Dict:
        """Delete an ingredient"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            query = "DELETE FROM ingredients WHERE id = :id"

            with engine.begin() as conn:
                conn.execute(text(query), {"id": ingredient_id})

            return {"message": "Ingredient deleted successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting ingredient: {str(e)}")

    @staticmethod
    def get_products(engine) -> Dict:
        """Get all products"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            query = """
                SELECT
                    id, product_name, product_type, selling_price,
                    description, is_active, created_at, updated_at
                FROM products
                WHERE is_active = TRUE
                ORDER BY product_name
            """

            df = pd.read_sql(query, engine)

            if df.empty:
                return {"products": []}

            products = df.to_dict('records')

            for product in products:
                product['selling_price'] = float(product['selling_price'])
                product['created_at'] = product['created_at'].isoformat() if product['created_at'] else None
                product['updated_at'] = product['updated_at'].isoformat() if product['updated_at'] else None

            return {"products": products}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

    @staticmethod
    def get_product_cost_analysis(engine, product_id: int) -> Dict:
        """Calculate cost breakdown and profit margin for a product"""
        if engine is None:
            raise HTTPException(status_code=500, detail="Database connection not available")

        try:
            query = """
                SELECT
                    p.id, p.product_name, p.selling_price,
                    SUM(pi.quantity_needed * i.unit_cost) as total_cost,
                    GROUP_CONCAT(CONCAT(i.name, ': ', pi.quantity_needed, ' ', i.unit) SEPARATOR ', ') as ingredients_used
                FROM products p
                LEFT JOIN product_ingredients pi ON p.id = pi.product_id
                LEFT JOIN ingredients i ON pi.ingredient_id = i.id
                WHERE p.id = %s
                GROUP BY p.id, p.product_name, p.selling_price
            """

            df = pd.read_sql(query, engine, params=(product_id,))

            if df.empty:
                raise HTTPException(status_code=404, detail="Product not found")

            result = df.iloc[0].to_dict()

            selling_price = float(result['selling_price'])
            total_cost = float(result['total_cost']) if result['total_cost'] else 0
            profit = selling_price - total_cost
            profit_margin = (profit / selling_price * 100) if selling_price > 0 else 0

            return {
                "product_id": result['id'],
                "product_name": result['product_name'],
                "selling_price": selling_price,
                "total_cost": total_cost,
                "profit": profit,
                "profit_margin": round(profit_margin, 2),
                "ingredients_used": result['ingredients_used']
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calculating cost: {str(e)}")
