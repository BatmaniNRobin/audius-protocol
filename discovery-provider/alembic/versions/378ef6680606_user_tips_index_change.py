"""User Tips Index Change

Revision ID: 378ef6680606
Revises: 8c10373f2615
Create Date: 2022-04-29 01:52:21.978573

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "378ef6680606"
down_revision = "8c10373f2615"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        op.f("ix_user_tips_slot"),
        "user_tips",
        ["slot"],
        unique=False,
        info={"if_not_exists": True},
    )
    op.drop_index(
        "ix_user_tips_signature", table_name="user_tips", info={"if_exists": True}
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        "ix_user_tips_signature",
        "user_tips",
        ["signature"],
        unique=False,
        info={"if_not_exists": True},
    )
    op.drop_index(
        op.f("ix_user_tips_slot"), table_name="user_tips", info={"if_exists": True}
    )
    # ### end Alembic commands ###
    pass