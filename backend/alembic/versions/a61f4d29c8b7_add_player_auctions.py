"""add player auctions

Revision ID: a61f4d29c8b7
Revises: 4e09b9eab350
Create Date: 2026-09-11 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


revision = "a61f4d29c8b7"
down_revision = "4e09b9eab350"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("participant", sa.Column("user_id", mysql.CHAR(length=36), nullable=True))
    op.add_column("participant", sa.Column("pending_user_email", sa.String(length=320), nullable=True))
    op.create_foreign_key(
        "fk_participant_user_id",
        "participant",
        "user",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_participant_user_id", "participant", ["user_id"], unique=False)
    op.create_index(
        "ix_participant_pending_user_email",
        "participant",
        ["pending_user_email"],
        unique=False,
    )
    op.create_unique_constraint(
        "uq_participant_championship_user",
        "participant",
        ["championship_id", "user_id"],
    )
    op.create_unique_constraint(
        "uq_participant_championship_pending_email",
        "participant",
        ["championship_id", "pending_user_email"],
    )

    op.add_column("draft_pick", sa.Column("championship_id", sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE draft_pick AS draft_pick_row
        INNER JOIN participant AS participant_row
            ON participant_row.id = draft_pick_row.participant_id
        SET draft_pick_row.championship_id = participant_row.championship_id
        """
    )
    op.alter_column(
        "draft_pick",
        "championship_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.create_foreign_key(
        "fk_draft_pick_championship_id",
        "draft_pick",
        "championship",
        ["championship_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        "uq_draft_pick_championship_player",
        "draft_pick",
        ["championship_id", "player_id"],
    )

    op.create_table(
        "player_auction",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("championship_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.String(length=255), nullable=False),
        sa.Column("deadline", sa.DateTime(), nullable=False),
        sa.Column("minimum_bid", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("open", "closed", "cancelled", name="player_auction_status"),
            server_default="open",
            nullable=False,
        ),
        sa.Column("leading_participant_id", sa.Integer(), nullable=True),
        sa.Column("leading_bid", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["championship_id"],
            ["championship.id"],
            name="fk_player_auction_championship_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
            name="fk_player_auction_player_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["leading_participant_id"],
            ["participant.id"],
            name="fk_player_auction_leading_participant_id",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "championship_id",
            "player_id",
            name="uq_player_auction_championship_player",
        ),
    )
    op.create_index(
        "ix_player_auction_status_deadline",
        "player_auction",
        ["status", "deadline"],
        unique=False,
    )

    op.create_table(
        "bid",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("auction_id", sa.Integer(), nullable=False),
        sa.Column("participant_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["auction_id"],
            ["player_auction.id"],
            name="fk_bid_auction_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["participant_id"],
            ["participant.id"],
            name="fk_bid_participant_id",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bid_auction_created_at", "bid", ["auction_id", "created_at"], unique=False)
    op.create_index("ix_bid_participant", "bid", ["participant_id"], unique=False)


def downgrade():
    op.drop_index("ix_bid_participant", table_name="bid")
    op.drop_index("ix_bid_auction_created_at", table_name="bid")
    op.drop_table("bid")

    op.drop_index("ix_player_auction_status_deadline", table_name="player_auction")
    op.drop_table("player_auction")

    op.drop_constraint("uq_draft_pick_championship_player", "draft_pick", type_="unique")
    op.drop_constraint("fk_draft_pick_championship_id", "draft_pick", type_="foreignkey")
    op.drop_column("draft_pick", "championship_id")

    op.drop_constraint(
        "uq_participant_championship_pending_email",
        "participant",
        type_="unique",
    )
    op.drop_constraint("uq_participant_championship_user", "participant", type_="unique")
    op.drop_index("ix_participant_pending_user_email", table_name="participant")
    op.drop_index("ix_participant_user_id", table_name="participant")
    op.drop_constraint("fk_participant_user_id", "participant", type_="foreignkey")
    op.drop_column("participant", "pending_user_email")
    op.drop_column("participant", "user_id")