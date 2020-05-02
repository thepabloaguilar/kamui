import pkgutil
import inspect
import importlib
from functools import partial
from types import ModuleType
from typing import Callable, Any, Generator

from punq import Container


di_container = Container()


def _get_sub_modules(module_path: str) -> Generator[ModuleType, None, None]:
    module = importlib.import_module(module_path)
    for __, sub_name, is_package in pkgutil.iter_modules(getattr(module, "__path__")):
        if is_package:
            yield importlib.import_module(f"{module_path}.{sub_name}.__init__")


def _register_classes(module_path: str, register: Callable[[Any], None]) -> None:
    for sub_module in _get_sub_modules(module_path):
        for name, clazz in inspect.getmembers(sub_module, inspect.isclass):
            register(clazz)


def _register_usecases(module_path: str, container: Container) -> None:
    _register_classes(module_path, container.register)


def _register_dataproviders(module_path: str, container: Container) -> None:
    # TODO: find a better way to do this verification before register
    def register(container_: Container, clazz: Any) -> None:
        class_to_register, first_parent_class, *__ = inspect.getmro(clazz)
        if inspect.isabstract(first_parent_class):
            container_.register(first_parent_class, class_to_register)

    _register_classes(module_path, partial(register, container))


_register_usecases("kamui.core.usecase", di_container)
_register_dataproviders("kamui.dataproviders.database", di_container)
_register_dataproviders("kamui.dataproviders.rest", di_container)
