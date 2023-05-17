from designs.decorator_base_strategy.strategies.test_director import (
    TestFixtureStrategyWithService,
    test_strategy_director,
)


@test_strategy_director.strategy()
def do_something(self, user_name, option_var):
    return {"user_name": user_name, "option_var": option_var}


@test_strategy_director.strategy(name="another_name")
def named_strategy(self, user_name, option_var):
    return {"named_strategy_user_name": user_name, "named_strategy_option_var": option_var}


@test_strategy_director.strategy(base=TestFixtureStrategyWithService)
def strategy_with_service(self, user_name, option_var):
    formatted_message = self._service.format_message(user_name)
    return {"strategy_with_service_user_name": formatted_message, "strategy_with_service_option_var": option_var}


@test_strategy_director.strategy(base=TestFixtureStrategyWithService)
def strategy_with_other_options_service(self, user_name: str, option_list: list = None, **kwargs):
    formatted_message = self._service.format_message(user_name)
    another_option = kwargs.get("another_option")

    result_dict = {
        "strategy_with_service_user_name": formatted_message,
        "strategy_with_service_option_var": option_list,
    }

    if another_option:
        result_dict["another_option"] = another_option

    return result_dict
