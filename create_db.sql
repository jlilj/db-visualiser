-- Create the 'test' schema
CREATE SCHEMA IF NOT EXISTS test;

-- Create the 'tbl_order' table
CREATE TABLE IF NOT EXISTS test.tbl_order (
    OrderID SERIAL PRIMARY KEY,
    OrderDate DATE,
    ShippingID INT
);

-- Create the 'tbl_order_line' table
CREATE TABLE IF NOT EXISTS test.tbl_order_line (
    OrderID INT REFERENCES test.tbl_order(OrderID),
    OrderLineID SERIAL PRIMARY KEY,
    SkuID INT,
    Quantity INT
);

-- Insert examples into 'tbl_order'
INSERT INTO test.tbl_order (OrderDate, ShippingID) VALUES
    ('2023-08-01', 1001),
    ('2023-08-02', 1002);

-- Insert examples into 'tbl_order_line' with linked 'OrderID'
INSERT INTO test.tbl_order_line (OrderID, SkuID, Quantity) VALUES
    (1, 101, 5),
    (1, 102, 3),
    (2, 201, 2),
    (2, 202, 4);

SELECT table_catalog, table_schema, table_name
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog','information_schema');