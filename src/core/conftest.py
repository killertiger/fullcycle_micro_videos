import pytest


@pytest.fixture(scope="session")
def django_db_keepdb(request) -> bool:
    from django.conf import settings
    return request.config.getvalue("reuse_db") or settings.TEST_KEEP_DB