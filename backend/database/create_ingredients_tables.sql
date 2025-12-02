-- Create ingredients table
CREATE TABLE IF NOT EXISTS ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    unit VARCHAR(50) NOT NULL,  -- e.g., 'grams', 'ml', 'pieces', 'kg'
    stock_quantity DECIMAL(10, 2) NOT NULL DEFAULT 0,
    reorder_level DECIMAL(10, 2) NOT NULL DEFAULT 0,
    unit_cost DECIMAL(10, 2) DEFAULT 0,  -- Cost per unit
    supplier VARCHAR(200),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create products table (for coffee products)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    product_type VARCHAR(50) NOT NULL,  -- e.g., 'Coffee', 'Tea', 'Pastry'
    selling_price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create product_ingredients junction table (product recipes)
CREATE TABLE IF NOT EXISTS product_ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    quantity_needed DECIMAL(10, 2) NOT NULL,  -- Quantity of ingredient needed per product unit
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
    UNIQUE KEY unique_product_ingredient (product_id, ingredient_id)
);

-- Insert sample ingredients
INSERT INTO ingredients (name, unit, stock_quantity, reorder_level, unit_cost, supplier) VALUES
('Coffee Beans (Arabica)', 'kg', 50, 10, 15.50, 'Premium Coffee Suppliers'),
('Milk (Whole)', 'liters', 100, 20, 2.50, 'Local Dairy Farm'),
('Sugar', 'kg', 30, 5, 1.20, 'Wholesale Foods'),
('Vanilla Syrup', 'ml', 5000, 1000, 0.02, 'Flavor Express'),
('Caramel Syrup', 'ml', 4500, 1000, 0.02, 'Flavor Express'),
('Chocolate Syrup', 'ml', 4000, 1000, 0.02, 'Flavor Express'),
('Whipped Cream', 'grams', 2000, 500, 0.01, 'Dairy Products Co'),
('Ice', 'kg', 25, 5, 0.50, 'Ice Factory'),
('Espresso Cups (Small)', 'pieces', 500, 100, 0.15, 'Packaging Supplies'),
('Coffee Cups (Medium)', 'pieces', 400, 100, 0.20, 'Packaging Supplies'),
('Coffee Cups (Large)', 'pieces', 350, 100, 0.25, 'Packaging Supplies'),
('Straws', 'pieces', 1000, 200, 0.02, 'Packaging Supplies'),
('Napkins', 'pieces', 2000, 500, 0.01, 'Packaging Supplies')
ON DUPLICATE KEY UPDATE name=name;

-- Insert sample products
INSERT INTO products (product_name, product_type, selling_price, description) VALUES
('Espresso', 'Coffee', 3.50, 'Classic espresso shot'),
('Americano', 'Coffee', 4.00, 'Espresso with hot water'),
('Cappuccino', 'Coffee', 4.50, 'Espresso with steamed milk and foam'),
('Latte', 'Coffee', 4.75, 'Espresso with steamed milk'),
('Iced Latte', 'Coffee', 5.00, 'Chilled latte with ice'),
('Caramel Latte', 'Coffee', 5.50, 'Latte with caramel syrup'),
('Vanilla Latte', 'Coffee', 5.50, 'Latte with vanilla syrup'),
('Mocha', 'Coffee', 5.75, 'Latte with chocolate syrup')
ON DUPLICATE KEY UPDATE product_name=product_name;

-- Insert sample product recipes (product_ingredients)
-- Espresso recipe
INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 0.018, 'Standard single shot'
FROM products p, ingredients i 
WHERE p.product_name = 'Espresso' AND i.name = 'Coffee Beans (Arabica)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 1, 'Small cup'
FROM products p, ingredients i 
WHERE p.product_name = 'Espresso' AND i.name = 'Espresso Cups (Small)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

-- Cappuccino recipe
INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 0.018, 'Double shot espresso'
FROM products p, ingredients i 
WHERE p.product_name = 'Cappuccino' AND i.name = 'Coffee Beans (Arabica)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 0.15, 'Steamed milk'
FROM products p, ingredients i 
WHERE p.product_name = 'Cappuccino' AND i.name = 'Milk (Whole)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 1, 'Medium cup'
FROM products p, ingredients i 
WHERE p.product_name = 'Cappuccino' AND i.name = 'Coffee Cups (Medium)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

-- Caramel Latte recipe
INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 0.018, 'Double shot espresso'
FROM products p, ingredients i 
WHERE p.product_name = 'Caramel Latte' AND i.name = 'Coffee Beans (Arabica)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 0.25, 'Steamed milk'
FROM products p, ingredients i 
WHERE p.product_name = 'Caramel Latte' AND i.name = 'Milk (Whole)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 30, 'Caramel syrup pump'
FROM products p, ingredients i 
WHERE p.product_name = 'Caramel Latte' AND i.name = 'Caramel Syrup'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 1, 'Large cup'
FROM products p, ingredients i 
WHERE p.product_name = 'Caramel Latte' AND i.name = 'Coffee Cups (Large)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

-- Mocha recipe
INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 0.018, 'Double shot espresso'
FROM products p, ingredients i 
WHERE p.product_name = 'Mocha' AND i.name = 'Coffee Beans (Arabica)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 0.25, 'Steamed milk'
FROM products p, ingredients i 
WHERE p.product_name = 'Mocha' AND i.name = 'Milk (Whole)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 30, 'Chocolate syrup'
FROM products p, ingredients i 
WHERE p.product_name = 'Mocha' AND i.name = 'Chocolate Syrup'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 20, 'Whipped cream topping'
FROM products p, ingredients i 
WHERE p.product_name = 'Mocha' AND i.name = 'Whipped Cream'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;

INSERT INTO product_ingredients (product_id, ingredient_id, quantity_needed, notes) 
SELECT p.id, i.id, 1, 'Large cup'
FROM products p, ingredients i 
WHERE p.product_name = 'Mocha' AND i.name = 'Coffee Cups (Large)'
ON DUPLICATE KEY UPDATE quantity_needed=quantity_needed;
