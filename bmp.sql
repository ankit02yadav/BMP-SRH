-- Database

CREATE DATABASE IF NOT EXISTS bmp;
USE bmp;

-- user tabel 

CREATE TABLE IF NOT EXISTS `users_bmp` (
  `id_user_bmp` int AUTO_INCREMENT PRIMARY KEY ,
  `username_bmp` varchar(255) NOT NULL,
  `password_bmp` varchar(255) NOT NULL,
  `full_name_bmp` varchar(255) NOT NULL
);

INSERT INTO users_bmp (username_bmp, password_bmp,full_name_bmp) VALUES
('ankit','ankit123',"Ankit Yadav"),
('abin','abin123',"Abin Shaji"),
('ishika','ishika123',"Ishika Nath"),
('azhaf','azhaf123',"azhaf"),
('dummy','dummy123',"Dummy Tester");

-- main table 

CREATE TABLE IF NOT EXISTS `Items_bmp` (
  `itemid_bmp` int NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `itemname_bmp` varchar(255) NOT NULL,
  `itemimage_bmp` varchar(255) DEFAULT NULL,
  `itemprice_bmp` int(11) NOT NULL ,
  `itemquantity_bmp` float NOT NULL 
);

INSERT INTO `Items_bmp` (itemname_bmp, itemimage_bmp, itemprice_bmp, itemquantity_bmp)
VALUES
('Chocolate Cake', './images/chocolate_cake.jpeg', 450, 15),
('Vanilla Pastry', './images/vanilla_pastry.jpeg', 120, 10),
('Croissant', './images/croissant.jpeg', 80, 20),
('Bread Loaf', './images/bread_loaf.jpeg', 60, 10),
('Blueberry Muffin', './images/blueberry_muffin.jpeg', 90, 12);

INSERT INTO `Items_bmp` (itemname_bmp, itemimage_bmp, itemprice_bmp, itemquantity_bmp)
VALUES
('Red Velvet Cake', './images/red_velvet_cake.jpeg', 500, 8),
('Apple Pie', './images/apple_pie.jpeg', 350, 10),
('Chocolate Donut', './images/chocolate_dont.jpeg', 50, 25),
('Glazed Donut', './images/glazed_donut.jpeg', 45, 30),
('Banana Bread', './images/banana_bread.jpeg', 200, 12),
('Cheesecake', './images/cheesecake.jpeg', 480, 6),
('Strawberry Tart', './images/strawberry_tart.jpeg', 220, 10),
('Brownie Fudge', './images/brownie_fudge.jpeg', 80, 20),
('Chocolate Eclair', './images/chocolate_eclair.jpeg', 90, 15),
('Cinnamon Roll', './images/cinamon_roll.jpeg', 60, 18),
('Garlic Bread Loaf', './images/garlic_bread_loaf.jpeg', 70, 10),
('Whole Wheat Bread', './images/whole_wheat_bread.jpeg', 65, 12),
('Multigrain Bread', './images/multigrain_bread.jpeg', 75, 10),
('Chocolate Chip Cookies', './images/chocolate_chip_cookies.jpeg', 100, 20),
('Cream Puff', './images/cream_puff.jpeg', 55, 15);

-- project name table

CREATE TABLE IF NOT EXISTS `header_bmp`(
  `header_id_bmp` int NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `heading_bmp` varchar(255) NOT NULL,
  `headingimage_bmp` varchar(255) NOT NULL
);
INSERT INTO `header_bmp` (heading_bmp, headingimage_bmp) VALUES ("Bakery Management Program (BMP)","./images/bms_logo.jpg");

-- customer_bmp
CREATE TABLE IF NOT EXISTS `customer_bmp`(
  `id_customer_bmp` int AUTO_INCREMENT PRIMARY KEY ,
  `username_bmp` varchar(255) NOT NULL,
  `password_bmp` varchar(255) NOT NULL,
  `full_name_bmp` varchar(255) NOT NULL
);

INSERT INTO customer_bmp (username_bmp, password_bmp,full_name_bmp) VALUES
('srk','ankit123','Shah Rukh Khan'),
('Hitler','hitler123','Adolf Hitler'),
('cr7','football','cristiano ronaldo'),
('messi','messi123','Lionel Andrés Messi Cuccittini'),
('dummy','dummy123',"Dummy Tester");

-- order id's

CREATE TABLE IF NOT EXISTS orders_bmp (
  order_id_bmp INT AUTO_INCREMENT PRIMARY KEY,
  customer_username_bmp VARCHAR(255) NOT NULL,
  order_date_bmp DATETIME DEFAULT CURRENT_TIMESTAMP,
  total_amount_bmp INT NOT NULL,
  payment_method_bmp VARCHAR(50) NOT NULL
);

INSERT INTO orders_bmp 
(customer_username_bmp, total_amount_bmp, payment_method_bmp)
VALUES
('srk', 630, 'Cash'),
('cr7', 250, 'Card'),
('dummy',900,'Cash');


-- itmes of every customer with id 

CREATE TABLE IF NOT EXISTS order_items_bmp (
  order_item_id_bmp INT AUTO_INCREMENT PRIMARY KEY,
  order_id_bmp INT NOT NULL,
  item_id_bmp INT NOT NULL,
  item_name_bmp VARCHAR(255) NOT NULL,
  quantity_bmp FLOAT NOT NULL,
  price_bmp INT NOT NULL,
  subtotal_bmp INT NOT NULL,
  FOREIGN KEY (order_id_bmp) REFERENCES orders_bmp(order_id_bmp),
  FOREIGN KEY (item_id_bmp) REFERENCES Items_bmp(itemid_bmp)
);

INSERT INTO order_items_bmp
(order_id_bmp, item_id_bmp, item_name_bmp, quantity_bmp, price_bmp, subtotal_bmp)
VALUES
-- Order 1 
(1, 1, 'Chocolate Cake', 1, 450, 450),
(1, 2, 'Vanilla Pastry', 1, 120, 120),
(1, 4, 'Bread Loaf', 1, 60, 60),

-- Order 2
(2, 3, 'Croissant', 2, 80, 160),
(2, 5, 'Blueberry Muffin', 1, 90, 90),

-- Order 3
(3, 1, 'Chocolate Cake', 2, 450, 900);
 