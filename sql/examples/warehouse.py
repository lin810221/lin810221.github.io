"""A real small star-schema build with half-open customer history and grain gates."""
def build_star(connection):
    connection.execute('BEGIN')
    try:
        connection.execute('''
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE analytics.dim_customer(customer_sk INTEGER PRIMARY KEY,customer_id INTEGER NOT NULL,
 region VARCHAR NOT NULL,valid_from TIMESTAMPTZ NOT NULL,valid_to TIMESTAMPTZ,
 CHECK(valid_to IS NULL OR valid_to>valid_from));
INSERT INTO analytics.dim_customer VALUES
 (1,1,'north','2026-01-01T00:00:00Z','2026-11-02T00:00:00Z'),
 (2,1,'south','2026-11-02T00:00:00Z',NULL),
 (3,2,'south','2026-01-01T00:00:00Z',NULL),
 (4,3,'north','2026-01-01T00:00:00Z',NULL),
 (5,4,'east','2026-01-01T00:00:00Z',NULL);
CREATE TABLE analytics.fact_order(order_id INTEGER PRIMARY KEY,customer_sk INTEGER REFERENCES analytics.dim_customer(customer_sk),
 order_day DATE NOT NULL,status VARCHAR NOT NULL,amount_cents BIGINT NOT NULL);
''')
        candidates='''SELECT o.order_id,d.customer_sk,CAST(o.created_at AS DATE) AS order_day,o.status,o.amount_cents
 FROM orders o JOIN analytics.dim_customer d ON d.customer_id=o.customer_id
 AND o.created_at>=d.valid_from AND (d.valid_to IS NULL OR o.created_at<d.valid_to)'''
        missing_or_multi=connection.execute('''SELECT o.order_id FROM orders o LEFT JOIN ('''+candidates+''') c USING(order_id)
 GROUP BY o.order_id HAVING COUNT(c.customer_sk)<>1''').fetchall()
        if missing_or_multi:raise ValueError('Each order must match exactly one historical dimension')
        connection.execute('INSERT INTO analytics.fact_order '+candidates)
        connection.execute('''CREATE VIEW analytics.mart_region AS SELECT d.region,COUNT(*) AS paid_orders,SUM(f.amount_cents) AS paid_cents
 FROM analytics.fact_order f JOIN analytics.dim_customer d ON d.customer_sk=f.customer_sk WHERE f.status='paid' GROUP BY d.region''')
        rows=connection.execute('SELECT * FROM analytics.mart_region ORDER BY region').fetchall()
        connection.execute('COMMIT');return rows
    except BaseException:
        connection.execute('ROLLBACK');raise
