SELECT
    CASE
        WHEN julianday(o.order_delivered_customer_date) >
             julianday(o.order_estimated_delivery_date)
        THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        AVG(
            julianday(o.order_delivered_customer_date) -
            julianday(o.order_purchase_timestamp)
        ), 2
    ) AS average_delivery_days,

    ROUND(AVG(r.review_score), 2) AS average_review_score

FROM orders o

LEFT JOIN reviews r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY delivery_status

ORDER BY delivery_status;
