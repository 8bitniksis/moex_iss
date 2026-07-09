import pytest

from moex_iss.exceptions import ISSServerError



def test_server_error():


    with pytest.raises(
        ISSServerError
    ):

        raise ISSServerError(
            503
        )