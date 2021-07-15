import logging
from abc import ABC, abstractmethod
from src.models import Challenge, UserChallenge

logger = logging.getLogger(__name__)

# DB Accessors
def fetch_user_challenges(session, challenge_id, user_ids):
    return (
        session.query(UserChallenge).filter(
            UserChallenge.challenge_id == challenge_id,
            UserChallenge.user_id.in_(user_ids),
        )
    ).all()


class ChallengeUpdater(ABC):
    """`ChallengeUpdater` is an abstract class which provides challenge specific logic
    to an instance of a `ChallengeManager`. The only required override is update_user_challenges
    """

    @abstractmethod
    def update_user_challenges(
        self, session, event, user_challenges_metadata, step_count
    ):
        """This is the main required method to fill out when implementing a new challenge.
        Given an event type, a list of existing user challenges, and the base challenge type,
        update the given user_challenges.
        """

    def on_after_challenge_creation(self, session, user_ids):
        """Optional method to do some work after the `ChallengeManager` creates new challenges.
        If a challenge is backed by it's own table, for instance, create those rows here.
        """

    def generate_specifier(self, user_id):
        """Optional method to provide a custom specifier for a challenge, given a user_id"""
        return user_id


class ChallengeManager:
    """`ChallengeManager` is responsible for handling shared logic between updating different challenges.
    To specialize a ChallengeManager for a particular challenge type, initialize it with a subclass
    of `ChallengeUpdater` implementing the business logic of that challenge.
    """

    def __init__(self, challenge_id, updater):
        self.challenge_id = challenge_id
        self._did_init = False
        self._updater = updater
        self._starting_block = None
        self._step_count = None

    def process(self, session, event_type, event_metadatas):
        """Processes a number of events for a particular event type, updating
        UserChallengeEvents as needed.

        event_metadata is [{ block_id: number, user_id: number }]
        """
        if not self._did_init:  # lazy init
            self._init_challenge(session)

        # filter out events that took place before the starting block, returning
        # early if need be
        if self._starting_block:
            event_metadatas = list(
                filter(
                    lambda x: x["block_number"] >= self._starting_block, event_metadatas
                )
            )

        if not event_metadatas:
            return

        user_ids = list(map(lambda x: x["user_id"], event_metadatas))
        user_id_metadatas = {x["user_id"]: x for x in event_metadatas}

        # Gets all user challenges,
        existing_user_challenges = fetch_user_challenges(
            session, self.challenge_id, user_ids
        )

        # Create users that need challenges still
        existing_user_ids = {
            challenge.user_id for challenge in existing_user_challenges
        }
        needs_challenge_ids = list(
            {id for id in user_ids if not id in existing_user_ids}
        )
        in_progress_challenges = [
            challenge
            for challenge in existing_user_challenges
            if not challenge.is_complete
        ]
        new_user_challenges = self._create_new_challenges(needs_challenge_ids)

        # Do any other custom work needed after creating a challenge event
        self._updater.on_after_challenge_creation(session, needs_challenge_ids)

        # Update all the challenges
        to_update = in_progress_challenges + new_user_challenges
        user_challenges_metadata = [
            (user_challenge, user_id_metadatas[user_challenge.user_id])
            for user_challenge in to_update
        ]
        self._updater.update_user_challenges(
            session, event_type, user_challenges_metadata, self._step_count
        )

        logger.debug(f"Updated challenges from event [{event_type}]: [{to_update}]")
        # Only add the new ones
        session.add_all(new_user_challenges)

    def get_challenge_state(self, session, user_ids):
        user_challenges = fetch_user_challenges(session, self.challenge_id, user_ids)
        return {
            user_challenge.user_id: user_challenge for user_challenge in user_challenges
        }

    # Helpers

    def _init_challenge(self, session):
        challenge = (
            session.query(Challenge).filter(Challenge.id == self.challenge_id).first()
        )
        if not challenge:
            raise Exception("No matching challenge!")
        self._starting_block = challenge.starting_block
        self._step_count = challenge.step_count
        self._did_init = True

    def _create_new_challenges(self, user_ids):
        return [
            UserChallenge(
                challenge_id=self.challenge_id,
                user_id=user_id,
                specifier=self._updater.generate_specifier(user_id),
                is_complete=False,
                current_step_count=0,
            )
            for user_id in user_ids
        ]