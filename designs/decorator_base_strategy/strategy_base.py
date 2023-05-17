from designs.decorator_base_strategy.strategies.director import BaseStrategy


class SomeService:
    """Simple class service for extension of Strategy base class"""

    @staticmethod
    def format_message(message):
        return f"hello {message}"


class StrategyWithService(BaseStrategy):
    """Simple class that override base Strategy for given access to external service"""

    _service = SomeService()

    def run(self) -> None:
        super(self).run()
