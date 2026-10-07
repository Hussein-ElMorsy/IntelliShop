from sqlalchemy import text
from app.db.session import engine


def check_database_connection() -> None:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        value = result.scalar_one()

        print(f"Database returned: {value}")


if __name__ == "__main__":
    check_database_connection()