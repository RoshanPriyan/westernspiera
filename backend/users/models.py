from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import hashlib
import base64
from database import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    users = relationship("UserModel", back_populates="role")
    

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    
    # ✅ Method to hash password before saving (alphanumeric only)
    def set_password(self, plain_password: str):
        hash_bytes = hashlib.sha256(plain_password.encode()).digest()
        b64_encoded = base64.b64encode(hash_bytes).decode('utf-8')
        self.password_hash = ''.join(filter(str.isalnum, b64_encoded))

    # ✅ Method to verify password
    def verify_password(self, plain_password: str) -> bool:
        hash_bytes = hashlib.sha256(plain_password.encode()).digest()
        b64_encoded = base64.b64encode(hash_bytes).decode('utf-8')
        return self.password_hash == ''.join(filter(str.isalnum, b64_encoded))
    
    role = relationship("RoleModel", back_populates="users")
