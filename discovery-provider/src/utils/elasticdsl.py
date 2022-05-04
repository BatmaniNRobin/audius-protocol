import copy
import os

from elasticsearch import Elasticsearch

es_url = os.getenv("audius_elasticsearch_url")
esclient = None
if es_url:
    esclient = Elasticsearch(es_url)


# uses aliases
ES_PLAYLISTS = "playlists"
ES_REPOSTS = "reposts"
ES_SAVES = "saves"
ES_TRACKS = "tracks"
ES_USERS = "users"


def listify(things):
    if isinstance(things, list):
        return [str(t) for t in things]
    return [str(things)]


def pluck_hits(found):
    return [h["_source"] for h in found["hits"]["hits"]]


def docs_and_ids(found, id_set=False):
    docs = []
    ids = []
    for hit in found["hits"]["hits"]:
        docs.append(hit["_source"])
        ids.append(hit["_id"])
    if id_set:
        ids = set(ids)
    return docs, ids


def hits_by_id(found):
    return {h["_id"]: h["_source"] for h in found["hits"]["hits"]}


def popuate_user_metadata_es(user, current_user):
    user_following = user.get("following_ids", [])
    current_user_following = current_user.get("following_ids", [])
    user["does_current_user_follow"] = user["user_id"] in current_user_following
    user["does_follow_current_user"] = current_user["user_id"] in user_following
    return omit_indexed_fields(user)


def populate_track_or_playlist_metadata_es(item, current_user):
    my_id = current_user["user_id"]
    item["has_current_user_reposted"] = my_id in item["reposted_by"]
    item["has_current_user_saved"] = my_id in item["saved_by"]
    return omit_indexed_fields(item)


omit_keys = [
    # user index
    "following_ids",
    "follower_ids",
    "tracks",
    # track index
    "reposted_by",
    "saved_by",
    # saves + reposts
    "item_key",
]


def omit_indexed_fields(doc):
    doc = copy.copy(doc)

    # track
    if "tags" in doc and isinstance(doc["tags"], list):
        doc["tags"] = ",".join(doc["tags"])

    if "following_count" in doc:
        doc["followee_count"] = doc["following_count"]

    for key in omit_keys:
        if key in doc:
            del doc[key]

    return doc