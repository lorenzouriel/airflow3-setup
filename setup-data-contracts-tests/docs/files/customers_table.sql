-- Drop table if exists
IF OBJECT_ID('dbo.customers', 'U') IS NOT NULL
    DROP TABLE dbo.customers;

-- Create the table
CREATE TABLE dbo.customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) NOT NULL,
    name NVARCHAR(100) NOT NULL,
    created_date DATETIME NOT NULL DEFAULT GETDATE(),
    updated_date DATETIME NOT NULL DEFAULT GETDATE(),
    total_purchases DECIMAL(10,2) NOT NULL DEFAULT 0,
    status NVARCHAR(50) NOT NULL
);

-- Insert fake data
INSERT INTO dbo.customers (email, name, created_date, updated_date, total_purchases, status)
VALUES
('alice@example.com', 'Alice Johnson', '2025-11-09 10:15:00', GETDATE(), 120.50, 'Active'),
('bob@example.com', 'Bob Smith', '2025-11-08 14:30:00', GETDATE(), 0, 'Inactive'),
('carol@example.com', 'Carol Davis', '2025-11-10 08:45:00', GETDATE(), 560.75, 'Active'),
('dave@example.com', 'Dave Wilson', '2025-11-07 11:20:00', DATEADD(day, -2, GETDATE()), 300.00, 'Pending'),
('eve@example.com', 'Eve Martin', '2025-11-10 12:00:00', GETDATE(), 45.90, 'Active');

-- Sample query
SELECT 
    customer_id,
    email,
    name,
    created_date,
    total_purchases,
    status
FROM dbo.customers
WHERE updated_date >= DATEADD(day, -1, GETDATE());
