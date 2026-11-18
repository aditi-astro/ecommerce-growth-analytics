SELECT
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    ROUND(SUM(oi.price), 2) AS product_sales,

    ROUND(AVG(oi.price), 2) AS average_item_price,

    ROUND(SUM(oi.freight_value), 2) AS freight_value

FROM order_items oi

JOIN orders o
    ON oi.order_id = o.order_id

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name

WHERE o.order_status = 'delivered'

GROUP BY category

ORDER BY product_sales DESC

LIMIT 15;
