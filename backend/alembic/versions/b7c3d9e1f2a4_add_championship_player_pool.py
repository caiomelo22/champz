"""add championship player pool

Revision ID: b7c3d9e1f2a4
Revises: a61f4d29c8b7
Create Date: 2026-10-29 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "b7c3d9e1f2a4"
down_revision = "a61f4d29c8b7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "championship_player",
        sa.Column("championship_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["championship_id"], ["championship.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["player_id"], ["player.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("championship_id", "player_id"),
    )


def downgrade():
    op.drop_table("championship_player")
