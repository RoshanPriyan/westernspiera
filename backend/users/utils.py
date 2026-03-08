from sqlalchemy import select
from users.models import RoleModel


async def get_user_role(role_id: int, session):
    get_role_exe = select(RoleModel).where(RoleModel.id == role_id)
    result = await session.execute(get_role_exe)
    role = result.scalars().one_or_none()
    return role.name
