import { useEffect, useState } from "react";
import { apiService } from "../../services/api";
import { Card } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Badge } from "../ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table";
import {
  Plus,
  Edit,
  Trash2,
  Package,
  AlertTriangle,
  DollarSign,
} from "lucide-react";
import { Textarea } from "../ui/textarea";

interface Ingredient {
  id: number;
  name: string;
  unit: string;
  stock_quantity: number;
  reorder_level: number;
  unit_cost: number;
  supplier: string;
  notes: string;
  is_low_stock: boolean;
}

interface Product {
  id: number;
  product_name: string;
  product_type: string;
  selling_price: number;
  description: string;
}

interface ProductIngredient {
  id: number;
  ingredient_id: number;
  ingredient_name: string;
  quantity_needed: number;
  unit: string;
  stock_quantity: number;
  units_available: number;
  notes: string;
}

export function IngredientsPage() {
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [productIngredients, setProductIngredients] = useState<
    ProductIngredient[]
  >([]);
  const [isAddingIngredient, setIsAddingIngredient] = useState(false);
  const [isAddingProduct, setIsAddingProduct] = useState(false);
  const [isAddingRecipe, setIsAddingRecipe] = useState(false);
  const [editingIngredient, setEditingIngredient] = useState<Ingredient | null>(
    null
  );
  const [activeTab, setActiveTab] = useState<"ingredients" | "products">(
    "ingredients"
  );

  const [newIngredient, setNewIngredient] = useState({
    name: "",
    unit: "kg",
    stock_quantity: 0,
    reorder_level: 0,
    unit_cost: 0,
    supplier: "",
    notes: "",
  });

  const [newProduct, setNewProduct] = useState({
    product_name: "",
    product_type: "Coffee",
    selling_price: 0,
    description: "",
  });

  const [newRecipe, setNewRecipe] = useState({
    ingredient_id: 0,
    quantity_needed: 0,
    notes: "",
  });

  useEffect(() => {
    fetchIngredients();
    fetchProducts();
  }, []);

  const fetchIngredients = async () => {
    try {
      const data = await apiService.getIngredients();
      setIngredients(data.ingredients || []);
    } catch (error) {
      console.error("Error fetching ingredients:", error);
    }
  };

  const fetchProducts = async () => {
    try {
      const data = await apiService.getProducts();
      setProducts(data.products || []);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const fetchProductIngredients = async (productId: number) => {
    try {
      const data = await apiService.getProductIngredients(productId);
      setProductIngredients(data.product_ingredients || []);
    } catch (error) {
      console.error("Error fetching product ingredients:", error);
    }
  };

  const handleAddIngredient = async () => {
    console.log("handleAddIngredient called with:", newIngredient);

    // Validate required fields
    if (!newIngredient.name.trim()) {
      alert("Please enter an ingredient name");
      return;
    }

    try {
      console.log("Sending request to API...");
      const result = await apiService.addIngredient(newIngredient);
      console.log("API response:", result);

      alert("Ingredient added successfully!");
      setIsAddingIngredient(false);
      setNewIngredient({
        name: "",
        unit: "kg",
        stock_quantity: 0,
        reorder_level: 0,
        unit_cost: 0,
        supplier: "",
        notes: "",
      });
      fetchIngredients();
    } catch (error) {
      console.error("Error adding ingredient:", error);
      alert(`Failed to add ingredient: ${error}`);
    }
  };

  const handleUpdateIngredient = async () => {
    if (!editingIngredient) return;

    try {
      await apiService.updateIngredient(
        editingIngredient.id,
        editingIngredient
      );
      setEditingIngredient(null);
      fetchIngredients();
    } catch (error) {
      console.error("Error updating ingredient:", error);
      alert(`Failed to update ingredient: ${error}`);
    }
  };

  const handleDeleteIngredient = async (id: number) => {
    if (!confirm("Are you sure you want to delete this ingredient?")) return;

    try {
      await apiService.deleteIngredient(id);
      fetchIngredients();
    } catch (error) {
      console.error("Error deleting ingredient:", error);
      alert(`Failed to delete ingredient: ${error}`);
    }
  };

  const handleAddProduct = async () => {
    console.log("handleAddProduct called with:", newProduct);

    // Validate required fields
    if (!newProduct.product_name.trim()) {
      alert("Please enter a product name");
      return;
    }

    try {
      console.log("Sending request to API...");
      const result = await apiService.addProduct(newProduct);
      console.log("API response:", result);

      alert("Product added successfully!");
      setIsAddingProduct(false);
      setNewProduct({
        product_name: "",
        product_type: "Coffee",
        selling_price: 0,
        description: "",
      });
      fetchProducts();
    } catch (error) {
      console.error("Error adding product:", error);
      alert(`Failed to add product: ${error}`);
    }
  };

  const handleAddRecipeIngredient = async () => {
    console.log("handleAddRecipeIngredient called");

    if (!selectedProduct) {
      alert("Please select a product first");
      return;
    }

    if (newRecipe.ingredient_id === 0) {
      alert("Please select an ingredient");
      return;
    }

    if (newRecipe.quantity_needed <= 0) {
      alert("Please enter a quantity greater than 0");
      return;
    }

    try {
      console.log("Sending request to API...");
      const result = await apiService.addProductIngredient(
        selectedProduct.id,
        newRecipe
      );
      console.log("API response:", result);

      alert("Ingredient added to recipe successfully!");
      setIsAddingRecipe(false);
      setNewRecipe({ ingredient_id: 0, quantity_needed: 0, notes: "" });
      fetchProductIngredients(selectedProduct.id);
    } catch (error) {
      console.error("Error adding recipe ingredient:", error);
      alert(`Failed to add to recipe: ${error}`);
    }
  };

  const handleRemoveRecipeIngredient = async (ingredientId: number) => {
    if (!selectedProduct) return;
    if (!confirm("Remove this ingredient from the recipe?")) return;

    try {
      await apiService.removeProductIngredient(
        selectedProduct.id,
        ingredientId
      );
      fetchProductIngredients(selectedProduct.id);
    } catch (error) {
      console.error("Error removing recipe ingredient:", error);
      alert(`Failed to remove ingredient: ${error}`);
    }
  };

  const selectProduct = (product: Product) => {
    setSelectedProduct(product);
    fetchProductIngredients(product.id);
  };

  const lowStockCount = ingredients.filter((i) => i.is_low_stock).length;

  return (
    <div className="p-8 bg-gradient-to-br from-[#eae7dc] to-[#d8c3a5] min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-[#8b5e3c] mb-2">
          Ingredient Management
        </h1>
        <p className="text-[#8b5e3c]/70">
          Manage ingredients, stock levels, and product recipes
        </p>
        {lowStockCount > 0 && (
          <div className="mt-4 p-4 bg-orange-100 border border-orange-300 rounded-lg flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-orange-600" />
            <span className="text-orange-800 font-semibold">
              {lowStockCount} ingredient{lowStockCount > 1 ? "s" : ""} below
              reorder level
            </span>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="flex gap-4 mb-6">
        <Button
          onClick={() => setActiveTab("ingredients")}
          className={
            activeTab === "ingredients"
              ? "bg-[#8b5e3c] text-white"
              : "bg-white text-[#8b5e3c] border border-[#8b5e3c]"
          }
        >
          <Package className="w-4 h-4 mr-2" />
          Ingredients
        </Button>
        <Button
          onClick={() => setActiveTab("products")}
          className={
            activeTab === "products"
              ? "bg-[#8b5e3c] text-white"
              : "bg-white text-[#8b5e3c] border border-[#8b5e3c]"
          }
        >
          <DollarSign className="w-4 h-4 mr-2" />
          Products & Recipes
        </Button>
      </div>

      {/* Ingredients Tab */}
      {activeTab === "ingredients" && (
        <Card className="p-6 bg-white/80 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-[#8b5e3c]">
              Ingredients Inventory
            </h2>
            <Button
              className="bg-[#8b5e3c] hover:bg-[#b08968] text-white"
              onClick={() => setIsAddingIngredient(true)}
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Ingredient
            </Button>
            <Dialog
              open={isAddingIngredient}
              onOpenChange={setIsAddingIngredient}
            >
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>Add New Ingredient</DialogTitle>
                  <DialogDescription>
                    Enter the details for the new ingredient
                  </DialogDescription>
                </DialogHeader>
                <div className="grid grid-cols-2 gap-4 py-4">
                  <div className="space-y-2">
                    <Label>Ingredient Name *</Label>
                    <Input
                      value={newIngredient.name}
                      onChange={(e) =>
                        setNewIngredient({
                          ...newIngredient,
                          name: e.target.value,
                        })
                      }
                      placeholder="e.g., Coffee Beans"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Unit *</Label>
                    <Select
                      value={newIngredient.unit}
                      onValueChange={(value) =>
                        setNewIngredient({ ...newIngredient, unit: value })
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="kg">Kilograms (kg)</SelectItem>
                        <SelectItem value="grams">Grams (g)</SelectItem>
                        <SelectItem value="liters">Liters (L)</SelectItem>
                        <SelectItem value="ml">Milliliters (ml)</SelectItem>
                        <SelectItem value="pieces">Pieces</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Stock Quantity *</Label>
                    <Input
                      type="number"
                      value={newIngredient.stock_quantity}
                      onChange={(e) =>
                        setNewIngredient({
                          ...newIngredient,
                          stock_quantity: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Reorder Level *</Label>
                    <Input
                      type="number"
                      value={newIngredient.reorder_level}
                      onChange={(e) =>
                        setNewIngredient({
                          ...newIngredient,
                          reorder_level: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Unit Cost ($)</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={newIngredient.unit_cost}
                      onChange={(e) =>
                        setNewIngredient({
                          ...newIngredient,
                          unit_cost: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Supplier</Label>
                    <Input
                      value={newIngredient.supplier}
                      onChange={(e) =>
                        setNewIngredient({
                          ...newIngredient,
                          supplier: e.target.value,
                        })
                      }
                      placeholder="Supplier name"
                    />
                  </div>
                  <div className="space-y-2 col-span-2">
                    <Label>Notes</Label>
                    <Textarea
                      value={newIngredient.notes}
                      onChange={(e) =>
                        setNewIngredient({
                          ...newIngredient,
                          notes: e.target.value,
                        })
                      }
                      placeholder="Additional notes..."
                    />
                  </div>
                </div>
                <DialogFooter>
                  <Button
                    variant="outline"
                    onClick={() => setIsAddingIngredient(false)}
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={handleAddIngredient}
                    className="bg-[#8b5e3c] hover:bg-[#b08968]"
                  >
                    Add Ingredient
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Stock</TableHead>
                <TableHead>Reorder Level</TableHead>
                <TableHead>Unit Cost</TableHead>
                <TableHead>Supplier</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ingredients.map((ingredient) => (
                <TableRow key={ingredient.id}>
                  <TableCell className="font-medium">
                    {ingredient.name}
                  </TableCell>
                  <TableCell>
                    {ingredient.stock_quantity} {ingredient.unit}
                  </TableCell>
                  <TableCell>
                    {ingredient.reorder_level} {ingredient.unit}
                  </TableCell>
                  <TableCell>${ingredient.unit_cost.toFixed(2)}</TableCell>
                  <TableCell>{ingredient.supplier || "-"}</TableCell>
                  <TableCell>
                    {ingredient.is_low_stock ? (
                      <Badge variant="destructive">Low Stock</Badge>
                    ) : (
                      <Badge className="bg-green-100 text-green-700">
                        In Stock
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setEditingIngredient(ingredient)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleDeleteIngredient(ingredient.id)}
                      >
                        <Trash2 className="w-4 h-4 text-red-600" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {/* Edit Ingredient Dialog */}
          <Dialog
            open={!!editingIngredient}
            onOpenChange={() => setEditingIngredient(null)}
          >
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Edit Ingredient</DialogTitle>
              </DialogHeader>
              {editingIngredient && (
                <div className="grid grid-cols-2 gap-4 py-4">
                  <div className="space-y-2">
                    <Label>Ingredient Name</Label>
                    <Input
                      value={editingIngredient.name}
                      onChange={(e) =>
                        setEditingIngredient({
                          ...editingIngredient,
                          name: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Unit</Label>
                    <Select
                      value={editingIngredient.unit}
                      onValueChange={(value) =>
                        setEditingIngredient({
                          ...editingIngredient,
                          unit: value,
                        })
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="kg">Kilograms (kg)</SelectItem>
                        <SelectItem value="grams">Grams (g)</SelectItem>
                        <SelectItem value="liters">Liters (L)</SelectItem>
                        <SelectItem value="ml">Milliliters (ml)</SelectItem>
                        <SelectItem value="pieces">Pieces</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Stock Quantity</Label>
                    <Input
                      type="number"
                      value={editingIngredient.stock_quantity}
                      onChange={(e) =>
                        setEditingIngredient({
                          ...editingIngredient,
                          stock_quantity: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Reorder Level</Label>
                    <Input
                      type="number"
                      value={editingIngredient.reorder_level}
                      onChange={(e) =>
                        setEditingIngredient({
                          ...editingIngredient,
                          reorder_level: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Unit Cost ($)</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={editingIngredient.unit_cost}
                      onChange={(e) =>
                        setEditingIngredient({
                          ...editingIngredient,
                          unit_cost: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Supplier</Label>
                    <Input
                      value={editingIngredient.supplier}
                      onChange={(e) =>
                        setEditingIngredient({
                          ...editingIngredient,
                          supplier: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="space-y-2 col-span-2">
                    <Label>Notes</Label>
                    <Textarea
                      value={editingIngredient.notes}
                      onChange={(e) =>
                        setEditingIngredient({
                          ...editingIngredient,
                          notes: e.target.value,
                        })
                      }
                    />
                  </div>
                </div>
              )}
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setEditingIngredient(null)}
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleUpdateIngredient}
                  className="bg-[#8b5e3c] hover:bg-[#b08968]"
                >
                  Update Ingredient
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </Card>
      )}

      {/* Products & Recipes Tab */}
      {activeTab === "products" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Products List */}
          <Card className="p-6 bg-white/80 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-[#8b5e3c]">Products</h2>
              <Button
                className="bg-[#8b5e3c] hover:bg-[#b08968] text-white"
                onClick={() => setIsAddingProduct(true)}
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Product
              </Button>
              <Dialog open={isAddingProduct} onOpenChange={setIsAddingProduct}>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Add New Product</DialogTitle>
                    <DialogDescription>
                      Fill in the product details. Fields marked with * are
                      required.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4 py-4">
                    <div className="space-y-2">
                      <Label>Product Name *</Label>
                      <Input
                        value={newProduct.product_name}
                        onChange={(e) =>
                          setNewProduct({
                            ...newProduct,
                            product_name: e.target.value,
                          })
                        }
                        placeholder="e.g., Caramel Macchiato"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Product Type *</Label>
                      <Select
                        value={newProduct.product_type}
                        onValueChange={(value) =>
                          setNewProduct({ ...newProduct, product_type: value })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Coffee">Coffee</SelectItem>
                          <SelectItem value="Tea">Tea</SelectItem>
                          <SelectItem value="Pastry">Pastry</SelectItem>
                          <SelectItem value="Other">Other</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Selling Price ($) *</Label>
                      <Input
                        type="number"
                        step="0.01"
                        value={newProduct.selling_price}
                        onChange={(e) =>
                          setNewProduct({
                            ...newProduct,
                            selling_price: parseFloat(e.target.value) || 0,
                          })
                        }
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>Description</Label>
                      <Textarea
                        value={newProduct.description}
                        onChange={(e) =>
                          setNewProduct({
                            ...newProduct,
                            description: e.target.value,
                          })
                        }
                        placeholder="Product description..."
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button
                      variant="outline"
                      onClick={() => setIsAddingProduct(false)}
                    >
                      Cancel
                    </Button>
                    <Button
                      onClick={handleAddProduct}
                      className="bg-[#8b5e3c] hover:bg-[#b08968]"
                    >
                      Add Product
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>

            <div className="space-y-3">
              {products.map((product) => (
                <div
                  key={product.id}
                  onClick={() => selectProduct(product)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    selectedProduct?.id === product.id
                      ? "border-[#8b5e3c] bg-[#8b5e3c]/10"
                      : "border-[#d8c3a5] hover:border-[#8b5e3c]/50"
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-[#8b5e3c]">
                        {product.product_name}
                      </h3>
                      <p className="text-sm text-[#8b5e3c]/60">
                        {product.product_type}
                      </p>
                    </div>
                    <span className="text-lg font-bold text-[#8b5e3c]">
                      ${product.selling_price.toFixed(2)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Product Recipe */}
          <Card className="p-6 bg-white/80 backdrop-blur-sm border-[#d8c3a5]/30 rounded-2xl">
            {selectedProduct ? (
              <>
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-[#8b5e3c]">
                      {selectedProduct.product_name} Recipe
                    </h2>
                    <p className="text-sm text-[#8b5e3c]/60">
                      Ingredients needed per unit
                    </p>
                  </div>
                  <Button
                    className="bg-[#8b5e3c] hover:bg-[#b08968] text-white"
                    onClick={() => setIsAddingRecipe(true)}
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Ingredient
                  </Button>
                  <Dialog
                    open={isAddingRecipe}
                    onOpenChange={setIsAddingRecipe}
                  >
                    <DialogContent>
                      <DialogHeader>
                        <DialogTitle>Add Ingredient to Recipe</DialogTitle>
                        <DialogDescription>
                          Select an ingredient and quantity needed per unit of
                          product.
                        </DialogDescription>
                      </DialogHeader>
                      <div className="space-y-4 py-4">
                        <div className="space-y-2">
                          <Label>Select Ingredient *</Label>
                          <Select
                            value={
                              newRecipe.ingredient_id > 0
                                ? newRecipe.ingredient_id.toString()
                                : ""
                            }
                            onValueChange={(value) =>
                              setNewRecipe({
                                ...newRecipe,
                                ingredient_id: parseInt(value),
                              })
                            }
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Choose an ingredient" />
                            </SelectTrigger>
                            <SelectContent>
                              {ingredients.map((ing) => (
                                <SelectItem
                                  key={ing.id}
                                  value={ing.id.toString()}
                                >
                                  {ing.name} ({ing.unit})
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="space-y-2">
                          <Label>Quantity Needed per Unit *</Label>
                          <Input
                            type="number"
                            step="0.001"
                            value={newRecipe.quantity_needed}
                            onChange={(e) =>
                              setNewRecipe({
                                ...newRecipe,
                                quantity_needed:
                                  parseFloat(e.target.value) || 0,
                              })
                            }
                            placeholder="e.g., 0.018 for 18g"
                          />
                        </div>
                        <div className="space-y-2">
                          <Label>Notes</Label>
                          <Textarea
                            value={newRecipe.notes}
                            onChange={(e) =>
                              setNewRecipe({
                                ...newRecipe,
                                notes: e.target.value,
                              })
                            }
                            placeholder="e.g., Double shot"
                          />
                        </div>
                      </div>
                      <DialogFooter>
                        <Button
                          variant="outline"
                          onClick={() => setIsAddingRecipe(false)}
                        >
                          Cancel
                        </Button>
                        <Button
                          onClick={handleAddRecipeIngredient}
                          className="bg-[#8b5e3c] hover:bg-[#b08968]"
                        >
                          Add to Recipe
                        </Button>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </div>

                <div className="space-y-3">
                  {productIngredients.length === 0 ? (
                    <p className="text-center text-[#8b5e3c]/60 py-8">
                      No ingredients added yet. Click "Add Ingredient" to create
                      the recipe.
                    </p>
                  ) : (
                    productIngredients.map((ing) => (
                      <div
                        key={ing.id}
                        className="p-4 rounded-lg border border-[#d8c3a5] bg-white"
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h4 className="font-semibold text-[#8b5e3c]">
                              {ing.ingredient_name}
                            </h4>
                            <p className="text-sm text-[#8b5e3c]/60">
                              {ing.quantity_needed} {ing.unit} per unit
                            </p>
                            {ing.notes && (
                              <p className="text-xs text-[#8b5e3c]/50 mt-1">
                                {ing.notes}
                              </p>
                            )}
                          </div>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              handleRemoveRecipeIngredient(ing.ingredient_id)
                            }
                          >
                            <Trash2 className="w-4 h-4 text-red-600" />
                          </Button>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <span className="text-[#8b5e3c]/60">
                            Can make: {ing.units_available} units
                          </span>
                          {ing.stock_quantity < ing.quantity_needed * 10 && (
                            <Badge variant="destructive" className="text-xs">
                              Low Stock
                            </Badge>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </>
            ) : (
              <div className="flex items-center justify-center h-full text-[#8b5e3c]/60">
                Select a product to view and edit its recipe
              </div>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}
