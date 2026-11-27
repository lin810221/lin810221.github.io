"""Small synthetic shop; all monetary amounts use integer USD cents."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent
SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL,
 region VARCHAR NOT NULL, email VARCHAR);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
 created_at TIMESTAMPTZ NOT NULL, status VARCHAR NOT NULL CHECK(status IN ('paid','cancelled')),
 amount_cents BIGINT NOT NULL CHECK(amount_cents>=0));
CREATE TABLE items(item_id INTEGER PRIMARY KEY, order_id INTEGER REFERENCES orders(order_id),
 product VARCHAR NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>0), unit_cents BIGINT NOT NULL CHECK(unit_cents>=0));
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER REFERENCES orders(order_id), amount_cents BIGINT NOT NULL CHECK(amount_cents>=0));
CREATE TABLE staff(id INTEGER PRIMARY KEY,parent_id INTEGER,name VARCHAR);
CREATE TABLE readings(id INTEGER PRIMARY KEY, day DATE, value INTEGER);
"""

def connect(path=':memory:'):
    connection=duckdb.connect(str(path),config={'threads':1,'autoinstall_known_extensions':False,'autoload_known_extensions':False})
    connection.execute("SET TimeZone='UTC'")
    return connection

def seed(connection):
    connection.execute(SCHEMA)
    connection.executemany('INSERT INTO customers VALUES (?,?,?,?)',[(1,'Ada','north','ada@example.test'),(2,'Bo','south',None),(3,'Cy','north','cy@example.test'),(4,'Dee','east',None)])
    connection.executemany('INSERT INTO orders VALUES (?,?,?,?,?)',[(101,1,'2026-11-01T09:00:00Z','paid',3000),(102,1,'2026-11-02T09:00:00Z','paid',5000),(103,2,'2026-11-02T09:00:00Z','cancelled',2000),(104,2,'2026-11-03T09:00:00Z','paid',4000),(105,3,'2026-11-03T09:00:00Z','paid',1000)])
    connection.executemany('INSERT INTO items VALUES (?,?,?,?,?)',[(1,101,'book',2,1500),(2,102,'pen',3,1000),(3,102,'notebook',1,2000),(4,103,'book',2,1000),(5,104,'mouse',2,2000),(6,105,'pen',1,1000)])
    connection.executemany('INSERT INTO refunds VALUES (?,?,?)',[(11,101,500),(12,102,1000),(13,102,500)])
    connection.executemany('INSERT INTO staff VALUES (?,?,?)',[(1,None,'lead'),(2,1,'engineering'),(3,2,'data'),(4,2,'web'),(5,1,'sales')])
    connection.executemany('INSERT INTO readings VALUES (?,?,?)',[(1,'2026-11-01',10),(2,'2026-11-02',None),(3,'2026-11-03',30),(4,'2026-11-04',40)])
    return connection

def query_file(connection,name):
    if not name.isdecimal() or len(name)!=2:raise ValueError('Two-digit lesson query name required')
    return connection.execute((ROOT/'queries'/f'{name}.sql').read_text(encoding='utf-8')).fetchall()
