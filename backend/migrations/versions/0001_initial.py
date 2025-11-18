"""accounts, posts, media

Revision ID: 0001
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(30), nullable=False, unique=True, index=True),
        sa.Column("full_name", sa.String(150)),
        sa.Column("biography", sa.Text),
        sa.Column("avatar_key", sa.String(200)),
        sa.Column("last_fetched_at", sa.DateTime),
        sa.Column("last_error", sa.Text),
        sa.Column("paused", sa.Boolean, nullable=False, server_default=sa.false()),