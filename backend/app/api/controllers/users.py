import logging
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.core.db import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, conn=Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    try:
        cur = conn.cursor()
        cur.execute("select * from users where email=%s", (user.email,))
        existing_user = cur.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exist")

        cur.execute(
            "insert into users(username ,email, password_hash) \
                values(%s,%s,%s) returning user_id, created_at",
            (user.username, user.email, hashed_password),
        )

        user_id, created_at = cur.fetchone()
        conn.commit()
        return UserResponse(
            user_id=user_id,
            username=user.username,
            email=user.email,
            created_at=created_at,
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/login")
def login_user():
    pass


@router.get("/users", response_model=list[UserResponse])
def get_users(conn=Depends(get_db)):
    stmt = "select user_id, username, email, created_at from users"
    cur = conn.cursor()
    cur.execute(stmt)
    rows = cur.fetchall()
    users = [
        UserResponse(
            user_id=row[0],
            username=row[1],
            email=row[2],
            created_at=row[3],
        )
        for row in rows
    ]
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, conn=Depends(get_db)):
    stmt = "select user_id, username, email, created_at from users where user_id = %s"
    cur = conn.cursor()
    cur.execute(stmt, (user_id,))
    row = cur.fetchone()
    return UserResponse(
        user_id=row[0],
        username=row[1],
        email=row[2],
        created_at=row[3],
    )


@router.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, conn=Depends(get_db)):
    try:
        cur = conn.cursor()
        cur.execute(
            "select user_id, username, email, created_at from users where user_id = %s",
            (user_id,)
        )
        existing_user = cur.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_fields = []
        update_values = []

        if user_update.username is not None:
            update_fields.append("username = %s")
            update_values.append(user_update.username)

        if user_update.email is not None:
            cur.execute("select user_id from users where email = %s and user_id != %s",
                        (user_update.email, user_id))
            if cur.fetchone():
                raise HTTPException(
                    status_code=400, detail="Email already in use")
            update_fields.append("email = %s")
            update_values.append(user_update.email)

        if user_update.password is not None:
            update_fields.append("password_hash = %s")
            update_values.append(user_update.password)

        if not update_fields:
            raise HTTPException(
                status_code=400, detail="No fields provided to update")

        update_values.append(user_id)
        update_query = f"update users set {
            ', '.join(update_fields)} where user_id = %s \
                returning user_id, username, email, created_at"

        cur.execute(update_query, tuple(update_values))
        updated_user = cur.fetchone()
        conn.commit()

        return UserResponse(
            user_id=updated_user[0],
            username=updated_user[1],
            email=updated_user[2],
            created_at=updated_user[3],
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{user_id}")
def delete_user(user_id: int, conn=Depends(get_db)):
    try:
        cur = conn.cursor()
        cur.execute("select * from users where user_id=%s", (user_id,))
        existing_user = cur.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User doesn't exist")

        cur.execute("delete from users where user_id=%s", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
