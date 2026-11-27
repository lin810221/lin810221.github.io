SELECT COUNT(*) AS customers, COUNT(email) AS known_emails,
       CAST('12.50' AS DECIMAL(12,2)) AS exact_amount,
       NULL = NULL AS unknown_equality,
       NULL IS NULL AS missing
FROM customers;
