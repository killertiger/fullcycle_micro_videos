from typing import List
import os
import pytest

def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        '--env',
        action='store',
        default='test',
        help="run tests using the specified env file from /envs folder",
    )
    
@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(
    early_config: pytest.Config,
    parser: pytest.Parser,
    args: List[str]
):
    parser_args = parser.parse_known_args(args)
    env = parser_args.env
    os.environ.setdefault('APP_ENV', env)
