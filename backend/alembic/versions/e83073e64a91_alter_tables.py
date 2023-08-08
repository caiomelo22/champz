"""alter_tables

Revision ID: e83073e64a91
Revises: 5764d768448d
Create Date: 2023-08-02 11:14:06.009406

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e83073e64a91"
down_revision = "5764d768448d"
branch_labels = None
depends_on = None


def upgrade():
    # Add the participant_id column to the team table
    op.add_column(
        "team",
        sa.Column(
            "participant_id",
            sa.Integer,
            sa.ForeignKey("participant.id", ondelete="SET NULL", onupdate="CASCADE"),
            nullable=True,
        ),
    )

    # Add the team_participant_id columns to the player table
    op.add_column(
        "player",
        sa.Column(
            "team_participant_id",
            sa.Integer,
            sa.ForeignKey("team.id", ondelete="SET NULL", onupdate="CASCADE"),
            nullable=True,
        ),
    )

    # Add the value columns to the player table
    op.add_column("player", sa.Column("value", sa.Integer, nullable=True))


def downgrade():
    # Remove the value column from the player table
    op.drop_column("player", "value")

    # Remove the team_participant_id and team_origin_id columns from the player table
    op.drop_column("player", "team_participant_id")

    # Remove the participant_id column from the team table
    op.drop_column("team", "participant_id")
