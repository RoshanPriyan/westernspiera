from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from users.schemas import UserSchema
from users.models import UserModel
from global_utils import success_response, CustomException


async def user_register_api(
        data: UserSchema,
        session: AsyncSession = Depends(get_db)
):
    try:
        user_name = data.username

        existing_user_stmt = select(UserModel).where(UserModel.username == user_name)
        existing_user_exe = await session.execute(existing_user_stmt)
        existing_user = existing_user_exe.scalars().one_or_none()

        if existing_user:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exist"
            )

        if data.confirm_password != data.password:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password and confirm password mismatch"
            )

        user = UserModel(username=data.username, email=data.email, role_id=2)
        user.set_password(data.password)
        session.add(user)
        await session.commit()

        return success_response(
            status_code=status.HTTP_201_CREATED,
            details="User register successfully"
        )

    except SQLAlchemyError as e:
        await session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
