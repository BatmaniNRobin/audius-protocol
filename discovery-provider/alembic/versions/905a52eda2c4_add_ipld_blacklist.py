"""add ipld blacklist

Revision ID: 905a52eda2c4
Revises: 23c4b650ed97
Create Date: 2019-03-20 11:36:28.566772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "905a52eda2c4"
down_revision = "23c4b650ed97"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ipld_blacklist_blocks",
        sa.Column("blockhash", sa.String(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=True),
        sa.Column("parenthash", sa.String(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("blockhash"),
        sa.UniqueConstraint("number"),
    )
    op.create_table(
        "ipld_blacklists",
        sa.Column("blockhash", sa.String(), nullable=False),
        sa.Column("blocknumber", sa.Integer(), nullable=False),
        sa.Column("ipld", sa.String(), nullable=False),
        sa.Column("is_blacklisted", sa.Boolean(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["blockhash"],
            ["ipld_blacklist_blocks.blockhash"],
        ),
        sa.ForeignKeyConstraint(
            ["blocknumber"],
            ["ipld_blacklist_blocks.number"],
        ),
        sa.PrimaryKeyConstraint("blockhash", "ipld", "is_blacklisted", "is_current"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ipld_blacklists")
    op.drop_table("ipld_blacklist_blocks")
    # ### end Alembic commands ###
