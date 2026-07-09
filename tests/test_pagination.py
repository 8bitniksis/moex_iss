from moex_iss.pagination import ISSPaginator


class MockClient:


    def __init__(self):

        self.calls=[]



    def get_json(
        self,
        url
    ):

        self.calls.append(url)


        if "start=0" in url:

            return {

                "history":{

                    "columns":[
                        "SECID"
                    ],

                    "data":[
                        ["SBER"],
                        ["GAZP"]
                    ]
                }

            }


        return {

            "history":{

                "columns":[
                    "SECID"
                ],

                "data":[]
            }

        }



def test_pagination():


    client = MockClient()


    paginator = ISSPaginator(
        client
    )


    rows=list(
        paginator.iterate(
            "http://test/history",
            "history"
        )
    )


    assert len(rows)==2


    assert (
        rows[0]["SECID"]
        ==
        "SBER"
    )


    assert len(client.calls)==2