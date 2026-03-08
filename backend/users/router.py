from fastapi import APIRouter
from users.services.user_register_api import user_register_api
from users.services.user_login_api import user_login_api


router = APIRouter(prefix="/api/v1/user", tags=["Users"])

router.add_api_route("/register", user_register_api, methods=["POST"])
router.add_api_route("/login", user_login_api, methods=["POST"])
