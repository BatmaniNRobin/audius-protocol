from typing import List, Optional, Tuple, TypedDict

from sqlalchemy.orm.session import Session
from src.models.models import User
from src.models.reaction import Reaction


class ReactionResponse(TypedDict):
    reaction_value: int
    reaction_type: str
    reacted_to: str
    sender_user_id: int


def get_reactions(
    session: Session, transaction_ids: List[str], type: Optional[str]
) -> List[ReactionResponse]:
    filters = [Reaction.reacted_to.in_(transaction_ids), User.is_current == True]
    if type:
        filters.append(Reaction.reaction_type == type)

    results: List[Tuple[Reaction, int]] = (
        session.query(Reaction, User.user_id)
        .join(User, User.wallet == Reaction.sender_wallet)
        .filter(
            *filters,
        )
        .all()
    )

    return [
        {
            "reaction_value": r.reaction_value,
            "reaction_type": r.reaction_type,
            "reacted_to": r.reacted_to,
            "sender_user_id": user_id,
        }
        for (r, user_id) in results
    ]