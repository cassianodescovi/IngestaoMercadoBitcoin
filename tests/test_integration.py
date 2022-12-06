import datetime
from apis import DaySummaryApi

class TestDaySummaryApi:
    def test_get_data(self):
        actual = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2021, 6, 1))
        expected = {"date": "2021-06-01", "opening": 193000, 
        "closing": 187999.99999, "lowest": 186400, "highest": 195729.99957, 
        "volume": "12889122.57094304", "quantity": "68.04365326",
         "amount": 7757, "avg_price": 189424.31735401}
        assert actual == expected

    def test_get_data_better(self):
        actual = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2021, 6, 1)).get("date")
        expected = "2021-06-01"
        assert actual == expected