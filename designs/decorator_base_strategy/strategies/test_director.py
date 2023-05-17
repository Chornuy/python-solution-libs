from unittest import mock

import pytest

from designs.decorator_base_strategy.strategies.director import BaseStrategy, StrategyDirector
from designs.decorator_base_strategy.strategies.test_base_strategy import TestFixtureStrategyWithService

TEST_STRATEGY_FIXTURES = ["designs.decorator_base_strategy.strategies.test_fixture_strategies"]
test_strategy_director = StrategyDirector(TEST_STRATEGY_FIXTURES)
test_strategy_director.load_strategies()


class TestStrategyDirector:
    @pytest.fixture
    def strategy_director_fixture(self) -> StrategyDirector:
        return test_strategy_director

    def test_director_loading(self, strategy_director_fixture: StrategyDirector):
        registered_strategies = strategy_director_fixture.get_strategies()
        assert "do_something" in registered_strategies
        assert "another_name" in registered_strategies
        assert "strategy_with_service" in registered_strategies

    def test_base_of_strategy_changes(self, strategy_director_fixture: StrategyDirector):
        strategy_obj = strategy_director_fixture.get_strategy_by_name("do_something")
        assert isinstance(strategy_obj, BaseStrategy)

        strategy_obj = strategy_director_fixture.get_strategy_by_name("strategy_with_service")
        assert isinstance(strategy_obj, TestFixtureStrategyWithService)
        assert hasattr(strategy_obj, "_service")

    def test_strategy_with_args_result(self, strategy_director_fixture: StrategyDirector):
        user_name = "John Doe"
        option_var = "test1"

        strategy_result = strategy_director_fixture.run_strategy("do_something", user_name, option_var)
        assert isinstance(strategy_result, dict)

        assert strategy_result["user_name"] == user_name
        assert strategy_result["option_var"] == option_var

    def test_strategy_result_with_kwargs_result(self, strategy_director_fixture: StrategyDirector):
        user_name = "John Doe"
        option_var = "test1"

        strategy_result = strategy_director_fixture.run_strategy(
            "do_something", user_name=user_name, option_var=option_var
        )

        assert isinstance(strategy_result, dict)

        assert strategy_result["user_name"] == user_name
        assert strategy_result["option_var"] == option_var

    @mock.patch("designs.decorator_base_strategy.strategies.test_base_strategy.TestingService.format_message")
    def test_strategy_called_a_service_method(self, mock_format_message, strategy_director_fixture: StrategyDirector):
        user_name = "John Doe"
        option_var = "test1"

        formatted_result = f"hello {user_name}"

        mock_format_message.return_value = formatted_result
        strategy_result = strategy_director_fixture.run_strategy(
            "strategy_with_service", user_name=user_name, option_var=option_var
        )

        mock_format_message.assert_called_with(user_name)
        mock_format_message.assert_called_once()

        assert isinstance(strategy_result, dict)

        assert strategy_result["strategy_with_service_user_name"] == formatted_result
        assert strategy_result["strategy_with_service_option_var"] == option_var

    def test_strategy_with_other_options_service(self, strategy_director_fixture: StrategyDirector):
        input_data = {
            "strategy": "strategy_with_other_options_service",
            "user_data": {"user_name": "test@gmail.com", "option_list": [1, 2, 3]},
        }
        strategy_result = strategy_director_fixture.run_strategy(input_data["strategy"], **input_data["user_data"])
        assert strategy_result["strategy_with_service_user_name"] == "hello test@gmail.com"
        assert strategy_result["strategy_with_service_option_var"] == [1, 2, 3]
        assert "another_option" not in strategy_result.keys()

    def test_strategy_with_none_option_list(self, strategy_director_fixture: StrategyDirector):
        input_data = {
            "strategy": "strategy_with_other_options_service",
            "user_data": {"user_name": "test@gmail.com", "another_option": "another_option"},
        }
        strategy_result = strategy_director_fixture.run_strategy(input_data["strategy"], **input_data["user_data"])

        assert strategy_result["strategy_with_service_user_name"] == "hello test@gmail.com"
        assert strategy_result["strategy_with_service_option_var"] is None
        assert "another_option" in strategy_result.keys()
        assert strategy_result["another_option"] == "another_option"
