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
            sa.ForeignKey("participant.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    # Add the team_participant column to the player table (now references participant's team name)
    op.add_column(
        "player",
        sa.Column(
            "team_participant",
            sa.String(255),
            nullable=True,
        ),
    )

    # Add the value columns to the player table
    op.add_column("player", sa.Column("value", sa.Integer, nullable=True))


def downgrade():
    # Remove the value column from the player table
    op.drop_column("player", "value")

    # Remove the team_participant column from the player table
    op.drop_column("player", "team_participant")

    # Remove the participant_id column from the team table
    op.drop_constraint("team_ibfk_1", "team", type_="foreignkey")
    op.drop_column("team", "participant_id")
