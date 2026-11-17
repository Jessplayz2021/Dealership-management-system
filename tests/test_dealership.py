import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import database as d
from main import parse_money, add_years_safe

VEHICLE = {'lot_number':'GOLF-001','make':'VW','model':'Golf R','year':2018,
'mileage':42000,'fuel':'Petrol','gearbox':'Automatic','colour':'Grey',
'intended_use':'Performance','price_pence':2250000,'engine_size':'2.0','drivetrain':'AWD'}

class DealershipTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name)/'test.db'
        d.setup_database(self.db)
        d.add_vehicle(VEHICLE, self.db)
    def tearDown(self): self.tmp.cleanup()
    def test_search(self):
        self.assertEqual(d.find_vehicles('golf-001', self.db)[0]['lot_number'], 'GOLF-001')
        self.assertEqual(len(d.find_vehicles('golf', self.db)), 1)
    def test_browse_filters(self):
        self.assertEqual(len(d.find_vehicles(path=self.db,available_only=True,filters={'max_price_pence':2300000,'fuel':'Petrol'})),1)
        self.assertEqual(len(d.find_vehicles(path=self.db,available_only=True,filters={'max_price_pence':2000000})),0)
    def test_sale_persists_and_cannot_repeat(self):
        sale = d.sell_vehicle('GOLF-001','Test Customer',self.db)
        self.assertEqual(sale, 1)
        self.assertEqual(d.get_vehicle('golf-001',self.db)['status'],'Sold')
        with self.assertRaises(ValueError): d.sell_vehicle('GOLF-001','Other',self.db)
        summary, rows = d.sales_summary(self.db)
        self.assertEqual(summary['revenue_pence'],2250000)
        self.assertEqual(len(rows),1)
        self.assertEqual(len(d.find_vehicles(path=self.db,available_only=True)),0)
    def test_repair_records(self):
        ticket = d.record_repair(150000,True,False,True,False,self.db)
        self.assertEqual(ticket,1)
        self.assertEqual(d.repair_summary(self.db)[0]['status'],'Awaiting workshop')
    def test_money(self):
        self.assertEqual(parse_money('£12,500.50'),1250050)
        for x in ('nan','12.345','-1','abc','0'):
            with self.assertRaises(ValueError): parse_money(x)
    def test_leap_year(self):
        self.assertEqual(add_years_safe(date(2024,2,29),1),date(2025,2,28))
    def test_unique_lot(self):
        with self.assertRaises(Exception): d.add_vehicle(VEHICLE,self.db)

if __name__=='__main__': unittest.main()
