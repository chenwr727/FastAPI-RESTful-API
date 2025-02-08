from starlette.exceptions import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, item_name: str, item_id: int):
        super().__init__(status_code=404, detail=f"{item_name} not found with ID: {item_id}")
