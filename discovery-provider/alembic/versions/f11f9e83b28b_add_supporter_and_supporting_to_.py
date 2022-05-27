"""Add supporter and supporting to aggregate user

Revision ID: f11f9e83b28b
Revises: 35198266d709
Create Date: 2022-05-11 08:10:57.138022

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f11f9e83b28b"
down_revision = "35198266d709"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "aggregate_user",
        sa.Column("supporter_count", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "aggregate_user",
        sa.Column("supporting_count", sa.Integer(), server_default="0", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("aggregate_user", "supporting_count")
    op.drop_column("aggregate_user", "supporter_count")
    # ### end Alembic commands ###