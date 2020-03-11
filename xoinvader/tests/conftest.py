"""Pytest configuration."""

import pytest

from eaf.state import State

from xoinvader import application


@pytest.fixture
def mock_application(request):

    app = None

    def inner():
        nonlocal app

        app = MockedApplication()
        return app

    request.addfinalizer(MockedApplication._finalize)
    return inner


@pytest.fixture
def mock_state(request, mock_application):

    app = None

    def inner(mock_app=False):
        nonlocal app

        if mock_app:
            # We need to create reference or object will be collected by gc
            app = mock_application()
        else:
            app = application.get_current()

        app.register(MockedState)
        return app.state

    def stop():
        app.deregister(MockedState.__name__)

    request.addfinalizer(stop)

    return inner


class MockedApplication(application.Application):

    @staticmethod
    def _finalize():
        try:
            app = application.get_current()
            app.stop()
            del app
        except:
            pass


class MockedState(State):
    pass
