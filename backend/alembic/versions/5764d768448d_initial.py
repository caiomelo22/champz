"""initial

Revision ID: 5764d768448d
Revises: 
Create Date: 2023-08-02 11:03:40.215139

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "5764d768448d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the participant table
    op.create_table(
        "participant",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("budget", sa.Integer, nullable=False),
    )

    # Create the group table
    op.create_table(
        "group",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
    )

    # Create the group_participant table
    op.create_table(
        "group_participant",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("group_id", sa.Integer, sa.ForeignKey("group.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "participant_id",
            sa.Integer,
            sa.ForeignKey("participant.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    # Create the match table
    op.create_table(
        "match",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("group_id", sa.Integer, sa.ForeignKey("group.id", ondelete="CASCADE"), nullable=True),
        sa.Column(
            "participant_1_id",
            sa.Integer,
            sa.ForeignKey("participant.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "participant_2_id",
            sa.Integer,
            sa.ForeignKey("participant.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("goals_1", sa.Integer, nullable=True),
        sa.Column("goals_2", sa.Integer, nullable=True),
        sa.Column("round", sa.Integer, nullable=True),
        sa.Column("penalties", sa.Boolean, nullable=True),
    )


def downgrade():
    # Drop the match table
    op.drop_table("match")

    # Drop the group_participant table
    op.drop_table("group_participant")

    # Drop the group table
    op.drop_table("group")

    # Drop the participant table
    op.drop_table("participant")
