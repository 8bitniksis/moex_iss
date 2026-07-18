import pytest

from moex_iss.utils.exceptions import ISSServerError


def test_server_error():

    with pytest.raises(ISSServerError):
        raise ISSServerError(503)
