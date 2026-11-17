"""SQLite storage for JS Spec Dealership. No third-party packages needed."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from datetime import datetime, timezone

DEFAULT_DB = Path(__file__).resolve().parent / 'dealership.db'

@contextmanager
def connect(path=DEFAULT_DB):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def setup_database(path=DEFAULT_DB):
    with connect(path) as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lot_number TEXT NOT NULL UNIQUE,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            mileage INTEGER NOT NULL CHECK(mileage >= 0),
            fuel TEXT NOT NULL,
            gearbox TEXT NOT NULL,
            colour TEXT NOT NULL,
            engine_size TEXT,
            drivetrain TEXT,
            intended_use TEXT NOT NULL,
            price_pence INTEGER NOT NULL CHECK(price_pence > 0),
            status TEXT NOT NULL DEFAULT 'Available'
                CHECK(status IN ('Available','Sold','Reserved'))
        );
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL UNIQUE REFERENCES vehicles(id),
            sold_at TEXT NOT NULL,
            sale_price_pence INTEGER NOT NULL CHECK(sale_price_pence > 0),
            customer_name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS repair_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            vehicle_price_pence INTEGER NOT NULL,
            starts INTEGER NOT NULL,
            makes_noise INTEGER NOT NULL,
            pulls_to_side INTEGER NOT NULL,
            drives_rough INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Awaiting workshop'
        );
        ''')

def add_vehicle(vehicle, path=DEFAULT_DB):
    fields = ('lot_number','make','model','year','mileage','fuel','gearbox',
              'colour','intended_use','price_pence','engine_size','drivetrain')
    with connect(path) as db:
        db.execute(f"INSERT INTO vehicles ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})",
                   tuple(vehicle.get(f) for f in fields))

def find_vehicles(term='', path=DEFAULT_DB, available_only=False, filters=None):
    term = term.strip()
    filters = filters or {}
    sql = "SELECT * FROM vehicles WHERE 1=1"
    params = []
    if term:
        sql += " AND (lot_number = ? COLLATE NOCASE OR make || ' ' || model LIKE ? COLLATE NOCASE OR model LIKE ? COLLATE NOCASE OR make LIKE ? COLLATE NOCASE)"
        params += [term, f'%{term}%', f'%{term}%', f'%{term}%']
    if available_only:
        sql += " AND status = 'Available'"
    if filters.get('max_price_pence') is not None:
        sql += " AND price_pence <= ?"
        params.append(filters['max_price_pence'])
    for key in ('gearbox', 'fuel', 'colour', 'intended_use'):
        if filters.get(key):
            sql += f' AND {key} LIKE ? COLLATE NOCASE'
            params.append('%' + filters[key] + '%')
    sql += ' ORDER BY year DESC, price_pence ASC, lot_number ASC'
    with connect(path) as db:
        return [dict(r) for r in db.execute(sql, params).fetchall()]

def get_vehicle(lot_number, path=DEFAULT_DB):
    with connect(path) as db:
        row = db.execute('SELECT * FROM vehicles WHERE lot_number = ? COLLATE NOCASE', (lot_number,)).fetchone()
        return dict(row) if row else None

def sell_vehicle(lot_number, customer_name, path=DEFAULT_DB):
    """Atomic sale: cannot sell a vehicle twice, including after a restart."""
    name = customer_name.strip()
    if not name:
        raise ValueError('Customer name is required.')
    with connect(path) as db:
        row = db.execute('SELECT id, price_pence FROM vehicles WHERE lot_number = ? COLLATE NOCASE', (lot_number,)).fetchone()
        if row is None:
            raise ValueError('That lot number does not exist.')
        updated = db.execute("UPDATE vehicles SET status='Sold' WHERE id=? AND status='Available'", (row['id'],))
        if updated.rowcount != 1:
            raise ValueError('That vehicle is not available for sale.')
        cur = db.execute('INSERT INTO sales (vehicle_id, sold_at, sale_price_pence, customer_name) VALUES (?, ?, ?, ?)',
                         (row['id'], datetime.now(timezone.utc).isoformat(timespec='seconds'), row['price_pence'], name))
        return cur.lastrowid

def sales_summary(path=DEFAULT_DB):
    with connect(path) as db:
        stats = db.execute('SELECT COUNT(*) AS sales, COALESCE(SUM(sale_price_pence), 0) AS revenue_pence FROM sales').fetchone()
        history = db.execute('''SELECT sales.id, sales.sold_at, sales.customer_name, sales.sale_price_pence,
                           vehicles.lot_number, vehicles.make, vehicles.model
                           FROM sales JOIN vehicles ON sales.vehicle_id = vehicles.id ORDER BY sales.id DESC''').fetchall()
        return dict(stats), [dict(r) for r in history]

def record_repair(price_pence, starts, makes_noise, pulls_to_side, drives_rough, path=DEFAULT_DB):
    with connect(path) as db:
        cur = db.execute('''INSERT INTO repair_requests
                           (created_at, vehicle_price_pence, starts, makes_noise, pulls_to_side, drives_rough)
                           VALUES (?, ?, ?, ?, ?, ?)''',
                         (datetime.now(timezone.utc).isoformat(timespec='seconds'), price_pence,
                          int(starts), int(makes_noise), int(pulls_to_side), int(drives_rough)))
        return cur.lastrowid

def repair_summary(path=DEFAULT_DB):
    with connect(path) as db:
        return [dict(r) for r in db.execute('SELECT * FROM repair_requests ORDER BY id DESC')]
