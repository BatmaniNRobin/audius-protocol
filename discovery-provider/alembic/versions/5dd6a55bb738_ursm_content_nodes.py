"""URSM content nodes

Revision ID: 5dd6a55bb738
Revises: 5aaa6198def8
Create Date: 2021-01-12 13:13:37.896953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5dd6a55bb738"
down_revision = "5aaa6198def8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ursm_content_nodes",
        sa.Column("blockhash", sa.String(), nullable=False),
        sa.Column("blocknumber", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("cnode_sp_id", sa.Integer(), nullable=False),
        sa.Column("delegate_owner_wallet", sa.String(), nullable=False),
        sa.Column("owner_wallet", sa.String(), nullable=False),
        sa.Column("proposer_sp_ids", sa.ARRAY(sa.Integer()), nullable=False),
        sa.Column("proposer_1_delegate_owner_wallet", sa.String(), nullable=False),
        sa.Column("proposer_2_delegate_owner_wallet", sa.String(), nullable=False),
        sa.Column("proposer_3_delegate_owner_wallet", sa.String(), nullable=False),
        sa.Column("endpoint", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["blockhash"],
            ["blocks.blockhash"],
        ),
        sa.ForeignKeyConstraint(
            ["blocknumber"],
            ["blocks.number"],
        ),
        sa.PrimaryKeyConstraint("is_current", "cnode_sp_id", "blockhash"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ursm_content_nodes")
    # ### end Alembic commands ###
