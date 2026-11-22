import hashlib
import hmac

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from config.config import ADMIN_PASSWORD

COOKIE_NAME = "glow_admin"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 дней

templates = Jinja2Templates("templates")
router = APIRouter(tags=["admin"])


def _token() -> str:
    # в cookie лежит не сам пароль, а подпись от него
    return hmac.new(ADMIN_PASSWORD.encode(), b"glow-admin", hashlib.sha256).hexdigest()


def is_admin(request: Request) -> bool:
    if not ADMIN_PASSWORD:
        return False
    cookie = request.cookies.get(COOKIE_NAME, "")
    return hmac.compare_digest(cookie.encode(), _token().encode())


async def require_admin(request: Request):
    if not is_admin(request):
        raise HTTPException(status_code=403, detail="admin only")


@router.get("/admin")
async def admin_page(request: Request, error: int = 0):
    return templates.TemplateResponse(
        request,
        "admin_login.html",
        {
            "request": request,
            "error": bool(error),
            "is_admin": is_admin(request),
            "configured": bool(ADMIN_PASSWORD),
        },
    )


@router.post("/admin/login")
async def admin_login(password: str = Form(...)):
    if ADMIN_PASSWORD and hmac.compare_digest(password.encode(), ADMIN_PASSWORD.encode()):
        response = RedirectResponse("/products#pricing", status_code=303)
        response.set_cookie(
            COOKIE_NAME, _token(), max_age=COOKIE_MAX_AGE, httponly=True, samesite="lax"
        )
        return response
    return RedirectResponse("/admin?error=1", status_code=303)


@router.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse("/products", status_code=303)
    response.delete_cookie(COOKIE_NAME)
    return response


@router.get("/api/admin/me")
async def admin_me(request: Request):
    return {"is_admin": is_admin(request)}
