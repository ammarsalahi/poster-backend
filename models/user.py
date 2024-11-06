from db import Base
from sqlalchemy.orm import Mapped,mapped_column
from uuid import UUID,uuid4

class User(Base):
    __tablename__="users"

    id:Mapped[UUID] = mapped_column(primary_key=True,default_factory=uuid4)

    personal_id:Mapped[str]=mapped_column(unique=True)

    fullname:Mapped[str]=mapped_column()

    phone:Mapped[str]=mapped_column(unique=True)

    password:Mapped[str]=mapped_column()

    created_at:Mapped[str]=mapped_column()

    updated_at:Mapped[str]=mapped_column()

    last_login:Mapped[str]=mapped_column()

    is_active:Mapped[bool]=mapped_column(default=False)

    is_superuser:Mapped[bool]=mapped_column(default=False)

