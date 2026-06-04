from fastapi import Request

from fastapi.responses import JSONResponse


# GLOBAL EXCEPTION
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc)
        }
    )