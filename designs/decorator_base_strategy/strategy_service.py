from designs.decorator_base_strategy.strategies.director import StrategyDirector

STRATEGY_MODULES = ["designs.decorator_base_strategy.concrete_strategy"]

strategy_director = StrategyDirector(look_up_modules=STRATEGY_MODULES)
strategy_director.load_strategies()
