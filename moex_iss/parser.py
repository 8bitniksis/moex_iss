from .models import ISSBlock



def parse_block(
    name: str,
    payload: dict
) -> ISSBlock:


    block = payload.get(name)


    if not block:
        raise ValueError(
            f"ISS block {name} missing"
        )


    return ISSBlock(

        name=name,

        columns=
            block.get(
                "columns",
                []
            ),

        data=
            block.get(
                "data",
                []
            ),

        metadata=
            block.get(
                "metadata",
                {}
            )
    )