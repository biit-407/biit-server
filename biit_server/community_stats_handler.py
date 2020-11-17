from biit_server.database import Database
from biit_server.azure import azure_refresh_token
from biit_server.query_helper import validate_query_params
from biit_server.http_responses import http401, jsonHttp200


def community_stats_get(request, community_id):
    """"""
    fields = ["email", "token"]

    # serializes the quert string to a dict (neeto)
    args = request.args

    query_validation = validate_query_params(args, fields)
    # check that body validation succeeded
    if query_validation[1] != 200:
        return query_validation

    auth = azure_refresh_token(args["token"])
    if not auth[0]:
        return http401("Not Authenticated")

    community_stats_db = Database("community_stats")

    response = {
        "access_token": auth[0],
        "refresh_token": auth[1],
        "data": community_stats_db.get(community_id).to_dict(),
    }

    return jsonHttp200("Community Stats Received", response)
