
# The Problem:

You need to store a lot of different logic. In my, it was around 20-40 different types of processing of data.
Depending on input data, and responses from third-party services, each strategy can set or behave them self differently based on the result


All strategies were categories base (each category can communicate with different services). Each category needs access
to different services, or share some common logic (for each category). The name of the strategy is unique.

Also, business was required to rapidly add new strategies, or remove old one. As an update existing on.

The solution:

Build some kind of Registry for each strategy.


```markdown
lib/strategy_director <- Base implementation of strategy Director
strategies/category1.py <- strategies for category 1
strategies/category2.py <- strategies for category 2
strategies/category2.py <- strategies for category 3
strategies/category2.py <- strategies for category 4
strategies/director.py <- Init of strategy director
```

Example of strategy:

```python
# strategies/category1.py
from designs.decorator_base_strategy.strategies.director import BaseStrategy
from designs.decorator_base_strategy.strategy_service import strategy_director


class Category1(BaseStrategy):

    service1 = Service1()
    service2 = Service2()

    def run(self) -> None:
        super().run()


@strategy_director.strategy(base=Category1)
def category1_strategy1(self, user_name, option_var):
    if self.service1.get(user_name, option_var):
        return do_something(user_name, option_var)

    return self.service2.call(user_name, option_var)


@strategy_director.strategy(base=Category1)
def category1_strategy2(self, user_name: str, option_var: list=None):
    do_something(user_name, option_var)
    return self.service2.get(user_name, option_var)

```
Example of registration of category and initialization register for strategies.


```python
from designs.decorator_base_strategy.strategies.director import StrategyDirector

STRATEGY_MODULES = [
   'strategies.category1', # path to python module where strategies store
   'strategies.category2'
]

# Init strategy register, setup modules to load
strategy_director = StrategyDirector(look_up_modules=STRATEGY_MODULES)

# Import all strategies from modules
strategy_director.load_strategies()

```


Example of call to process:

```python
from enum import Enum
from designs.decorator_base_strategy import strategy_director

class StrategyCategory(str, Enum):

    category1 = "category1"
    category2 = "category2"
    category3 = "category3"
    category4 = "category4"


def process_strategy():
    input_data = {
        "strategy_category": StrategyCategory.category1,
        "strategy_name": "strategy2",
        "user_data": {
            "user_name": "user@test.com",
            "options": [1,2,3]
        }
    }

    strategy_name = f"{input_data['strategy_category']}_{input_data['strategy_name']}"
    user_data = input_data['user_data']

    result = strategy_director.run_strategy(strategy_name, **user_data)
    return result

```

Resume:

Plus:
1) To find the strategy you can look for a name of the strategy to find a function by a name. The end business code will be there.
2) Adding a new common strategy much faster.
3) Split responsibility:
   * StrategyDirector - responsible for registering and running a strategy.
   * BaseStrategy - responsible for sharing services or common codes that need for all Strategies.
   * Category1(BaseStrategy) - responsible for sharing services and common code for each category.
   * Decorated function strategy - responsible for end logic for processing the data.
4) Strategy register load strategy on import of object. No need to create a manual object of strategy
5) Finding strategy in register take O(1) because of using of Dictionary.

Cons:
1) Loading and registration of strategy a little complicate mechanism. It needs knowledge decorators and the creation
of classes by using the function `type()`.
2) Need to remember to update the `STRATEGY_MODULES` variable to add a new category for strategy.
3) Memory consumption of the Dict type base, with all objects of strategies inside it will grow, with a number of strategies.
Can be improved by using ProxyObject, or LazyLoad for strategy.
