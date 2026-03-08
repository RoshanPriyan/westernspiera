from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from users.schemas import UserLoginSchema
from users.models import UserModel
from users.utils import get_user_role
from global_utils import success_response, CustomException, generate_token


async def user_login_api(
        data: UserLoginSchema,
        session: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(UserModel).where(UserModel.username == data.username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.verify_password(data.password):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
            
        role = await get_user_role(user.role_id, session)
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "role": role
            }

        token = generate_token(user_data)
        user_data["email"] = user.email
        user_data["token"] = token
        
        return success_response(
            status_code=status.HTTP_200_OK,
            details="User login successfully",
            data=user_data
        )

    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
