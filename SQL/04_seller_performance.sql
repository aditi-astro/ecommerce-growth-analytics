SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    COUNT(oi.order_item_id) AS total_items_sold,

    ROUND(SUM(oi.price), 2) AS product_sales,

    ROUND(AVG(oi.price), 2) AS average_item_price,

    ROUND(SUM(oi.freight_value), 2) AS freight_value

FROM sellers s

JOIN order_items oi
    ON s.seller_id = oi.seller_id

JOIN orders o
    ON oi.order_id = o.order_id

WHERE o.order_status = 'delivered'

GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state

ORDER BY product_sales DESC

LIMIT 20;
