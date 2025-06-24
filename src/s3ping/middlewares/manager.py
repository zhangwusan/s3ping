from typing import List
from src.s3ping.types.base import NextHandlerType, RequestType, ResponseType
from src.s3ping.middlewares.base import BaseMiddleware


class MiddlewareManager:
    def __init__(self, middlewares: List[BaseMiddleware]):
        self.middlewares = middlewares

    def execute(self, request: RequestType, final: NextHandlerType) -> ResponseType:
        """
        Chains middleware and calls the final (usually an engine.send).

        :param request: The request object to process.
        :param final: The final handler to call after all middleware.
        :return: Response from the final handler or middleware chain.
        """

        def wrap(index: int) -> NextHandlerType:
            if index >= len(self.middlewares):
                return final  # Final step: send request

            middleware = self.middlewares[index]

            def next_middleware(req: RequestType) -> ResponseType:
                return middleware.process(req, wrap(index + 1))

            return next_middleware

        # Start the middleware chain with index 0
        return wrap(0)(request)