import datetime
from abc import ABC, abstractmethod
from typing import List

from mercado_bitcoin.apis import DaySummaryApi
from mercado_bitcoin.checkpoints import DynamoCheckpoints, CheckpointModel


class DataIngestor(ABC):

    def __init__(self, writer, coins: List[str], default_start_date: datetime.date) -> None:
        self.default_start_date = default_start_date
        self.coins = coins
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    @property
    def _checkpoint_filename(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self._checkpoint}")

    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return self.default_start_date

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()

    @abstractmethod
    def ingest(self) -> None:
        pass


class DaySummaryIngestor(DataIngestor):

    def ingest(self) -> None:
        date = self._load_checkpoint()
        if date < datetime.datetime.now(datetime.timezone.utc).date():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))


class AwsDataIngestor:
    def __init__(self, writer, coins: List[str], default_start_date: datetime.date) -> None:
        self.dynamo_checkpoint = DynamoCheckpoints(
            model=CheckpointModel,
            report_id=self.__class__.__name__,
            default_start_date=default_start_date)
        self.default_start_date = default_start_date
        self.coins = coins
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    def _write_checkpoint(self):
        self.dynamo_checkpoint.create_checkpoint(checkpoint_date=self._checkpoint)

    def _load_checkpoint(self) -> datetime.date:
        return self.dynamo_checkpoint.get_checkpoint()

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self.dynamo_checkpoint.create_or_update_checkpoint(checkpoint_date=self._checkpoint)

    @abstractmethod
    def ingest(self) -> None:
        pass


class AwsDaySummaryIngestor(AwsDataIngestor):

    def ingest(self) -> None:
        date = self._load_checkpoint()
        if date < datetime.datetime.now(datetime.timezone.utc).date():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))