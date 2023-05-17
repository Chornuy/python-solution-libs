from designs.decorator_base_strategy.strategy_base import StrategyWithService
from designs.decorator_base_strategy.strategy_service import strategy_director


@strategy_director.strategy()
def do_something(self, user_name: str, option_var: str = None) -> dict:
    """Simple test example of strategy. This strategy will be registered under name of function.

    Args:
        self (BasicTask): bind strategy object
        user_name (str): example argument
        option_var (str): example argument

    Returns:
        dict: with arguments that was passed to a strategy.
    """
    return {"user_name": user_name, "option_var": option_var}


@strategy_director.strategy(name="another_name")
def named_strategy(self, user_name: str, option_var: str = None) -> dict:
    """Simple test strategy with custom name.
    This strategy will be registered under the name, that set in decorator options.

    Args:
        self (BasicTask): bind strategy object
        user_name (str): example argument
        option_var (str): example argument

    Returns:
        dict: with arguments that was passed to a strategy.
    """
    return {"named_strategy_user_name": user_name, "named_strategy_option_var": option_var}


@strategy_director.strategy(base=StrategyWithService)
def strategy_with_service(self, user_name: str, option_var: str = None) -> dict:
    """Simple test strategy with custom name.
    This strategy will be registered under the name, that set in decorator options.

    Args:
        self (BasicTask): bind strategy object
        user_name (str): example argument
        option_var (str): example argument

    Returns:
        dict: with arguments that was passed to a strategy.
    """
    formatted_message = self._service.format_message(user_name)
    return {"strategy_with_service_user_name": formatted_message, "strategy_with_service_option_var": option_var}
