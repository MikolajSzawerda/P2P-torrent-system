import inspect
import logging

logger = logging.getLogger(__name__)


class UndefinedRouteError(Exception):
    def __init__(self, route: str) -> None:
        super().__init__(f"Route {route} is not defined.")


class RoutesRegistry:
    def __init__(self) -> None:
        self._routes = {}
        self._route_args = {}

    def register(self, route: str):
        def inner(func):
            self._routes[route] = func
            self._route_args[route] = set(inspect.signature(func).parameters)
            return func

        return inner

    async def run_handler(self, route: str, **kwargs) -> None:
        if route not in self._routes:
            raise UndefinedRouteError(route)

        args = {
            arg: val for arg, val in kwargs.items() if arg in self._route_args[route]
        }

        await self._routes[route](**args)
