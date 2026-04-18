import contextvars
import functools
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable

__all__ = ["ContextSafeThreadPoolExecutor"]


class ContextSafeThreadPoolExecutor(ThreadPoolExecutor):
    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        ctx = contextvars.copy_context()

        return super().submit(functools.partial(ctx.run, functools.partial(fn, *args, **kwargs)))
