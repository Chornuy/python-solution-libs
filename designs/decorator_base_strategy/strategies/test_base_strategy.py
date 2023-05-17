from designs.decorator_base_strategy.strategies.director import BaseStrategy


class TestingService:
    """Simple class service for extension of Strategy base class"""

    __test__ = False

    @staticmethod
    def format_message(message):
        return f"hello {message}"


class TestFixtureStrategyWithService(BaseStrategy):
    """Simple class for tests that imitated strategy with service. Which will be call inside strategy function"""

    __test__ = False

    _service = TestingService()

    def run(self) -> None:
        super().run()
