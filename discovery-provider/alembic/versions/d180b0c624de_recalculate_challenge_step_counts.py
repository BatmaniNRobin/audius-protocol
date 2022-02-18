"""Recalculate challenge step counts

Revision ID: d180b0c624de
Revises: d3325cbc0bec
Create Date: 2022-02-16 17:05:48.186215

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d180b0c624de"
down_revision = "d3325cbc0bec"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute(
        """
        BEGIN;

        CREATE INDEX IF NOT EXISTS user_challenges_challenge_idx ON user_challenges (challenge_id);

        -- 'mobile-install' challenge only exists if completed
        -- 'connect-verified' challenge only exists if completed
        -- 'tt' (trending) challenge only exists if completed
        -- 'tut' (trending) challenge only exists if completed
        -- 'tp' (trending) challenge only exists if completed
        UPDATE user_challenges
        SET
            is_complete=True,
            current_step_count=1
        WHERE
            challenge_id='mobile-install' OR
            challenge_id='connect-verified' OR
            challenge_id='tt' OR
            challenge_id='tut' OR
            challenge_id='tp';

        WITH track_uploads AS (
            SELECT count(*) AS track_count, owner_id
            FROM tracks
            WHERE
                is_current=True AND
                blocknumber >= 25346436
            GROUP BY owner_id
        )
        UPDATE user_challenges
        SET
            is_complete=(track_uploads.track_count >= 3),
            current_step_count=track_uploads.track_count
        FROM
            track_uploads
        WHERE
            challenge_id='track-upload' AND
            user_id=owner_id;

        COMMIT;
        """
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###