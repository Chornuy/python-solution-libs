from collections.abc import Callable
from importlib import import_module
from typing import Any


class BaseStrategy:
    """Simple class for storing method, that decorate run method."""

    def __init__(self, *args, **kwargs) -> None:
        """

        Args:
            *args:
            **kwargs:
        """
        pass

    def run(self) -> None:
        """Run method will be overriden on calling

        Returns:

        """
        raise NotImplementedError(f"Object of {self.__name__}, must implement method run")


class StrategyDirector:
    """Class for storing and managing a different approaches of processing the data.
    The mechanic and main idea of this was taken from Celery library: https://github.com/celery/celery

    This class behave mostly the same way as Celery app load tasks.
    BaseStrategy class similar ot Task class of Celery.
    As Strategy Director similar to Celery app class.

    Examples:


    """

    base_strategy_cls = BaseStrategy

    def __init__(self, look_up_modules: list[str] = None) -> None:
        """Init method.

        Args:
            look_up_modules (list): List of str with modules where strategies are stored.
        """
        self.strategies_modules = look_up_modules if look_up_modules else []
        self.strategies = {}

    def load_strategies(self) -> None:
        """Load strategies, using an importlib.
        Returns:
            None:
        """
        for strategy_module in self.strategies_modules:
            import_module(strategy_module)

    def get_base_cls(self) -> type[BaseStrategy]:
        """Return cls of current base class for strategy

        Returns:
            cls: Base class of strategy

        """
        return self.base_strategy_cls

    def get_strategies(self) -> list[type[BaseStrategy]]:
        """Return list of registered names for strategies

        Returns:
            list[str]: list of registered strategies

        """
        return list(self.strategies.keys())

    def get_strategy_by_name(self, name: str) -> type[BaseStrategy] | None:
        """Return registered Strategy object by name, or None if no such strategy was registered.

        Args:
            name(str): name of strategy

        Returns:
            BaseStrategy: if such strategy exists
            None: strategy was not found

        """
        try:
            return self.strategies[name]
        except KeyError:
            return None

    def strategy(self, **strategy_options: Any) -> Callable:
        """Decorator for registering a strategy. Options are key value storage, for modification of creation class of
        strategy.

        Args:
            **strategy_options: Option for modification creation of strategy

        Returns:
            Callable: function decorator for registering a strategy
        """
        strategy_name = strategy_options.get("name", None)
        base_cls = strategy_options["base"] if "base" in strategy_options else self.get_base_cls()

        def create_inner_class(strategy_function: Callable, *args: Any, **kwargs: Any) -> None:
            """Decorated function. That create an object of BaseStrategy class or subclass of BaseStrategy class.

            Args:
                strategy_function (Callable):

            Returns:
                None
            """
            name = strategy_name if strategy_name else strategy_function.__name__
            self.strategies[name] = type(
                name,
                (base_cls,),
                {
                    "name": name,
                    "run": strategy_function,
                    "__doc__": strategy_function.__doc__,
                    "__module__": strategy_function.__module__,
                    "__annotations__": strategy_function.__annotations__,
                    "__wrapped__": strategy_function,
                },
            )(*args, **kwargs)

        return create_inner_class

    def run_strategy(self, strategy_name: str, *args: Any, **kwargs: Any):
        """Method take strategy by name from register of strategy,
        passing arguments to strategy method and retun result

        Args:
            strategy_name:
            *args:
            **kwargs:

        Returns:
            Any: result of method run of Strategy
        """
        return self.strategies[strategy_name].run(*args, **kwargs)
