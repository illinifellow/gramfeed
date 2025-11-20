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
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        "posts",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("shortcode", sa.String(20), nullable=False),
        sa.Column("taken_at", sa.DateTime, nullable=False, index=True),
        sa.Column("caption", sa.Text),
        sa.Column("kind", sa.String(10), nullable=False),
        sa.Column("location", sa.String(200)),
        sa.UniqueConstraint("account_id", "shortcode"),
    )
    op.create_table(
        "media",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("post_id", sa.BigInteger, sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("position", sa.Integer, nullable=False),
        sa.Column("kind", sa.String(10), nullable=False),
        sa.Column("key", sa.String(200), nullable=False),
        sa.Column("width", sa.Integer),