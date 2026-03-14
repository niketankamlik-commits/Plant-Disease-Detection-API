from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pathlib

router = APIRouter()
frontend_dir = pathlib.Path("frontend")

@router.get("/info", response_class=HTMLResponse)
def get_info_page():
    html_path = frontend_dir / "info.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text('utf-8'), status_code=200)
    return {"Error": "Info page not found"}
