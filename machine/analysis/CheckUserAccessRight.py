from machine.analysis.CreateConnectionToDB import get_db_connection


def GetBrainIfAuthorized(Brain_ID,
                         User_ID=None,
                         API=None,
                         for_solve=False):
    """
    Get brain object by user API key


    :param User_ID: user id
    :param for_solve: flag to decide which parameters from brain we need to select
    :param API: user API key
    :param Brain_ID: target brain id to get
    :return: brain object if access accept, else None
    """

    AI_cursor = get_db_connection(AI_CURSOR=True)

    column_properties_from_db = ['AnalysisSource_ColumnsNameInput', 'AnalysisSource_ColumnsNameOutput',
                                 'Data_ColumnsInputFilterLines']
    properties_from_db_for_solving = ['AnalysisSource_ColumnType', 'ParameterCNN_Loss', 'ParameterCNN_Optimizer',
                                      'Training_BrainModel', 'Training_BrainWeights', 'EncDec_ColumnsInputInformations',
                                      'EncDec_ColumnsOutputInformations']

    # Create sql to specify what need to get from DB
    if for_solve:
        properties_to_get_from_braindata = ', '.join(properties_from_db_for_solving + column_properties_from_db)
    else:
        properties_to_get_from_braindata = ', '.join(column_properties_from_db)

    # Create sql to check if user is authorized
    # If in function we get a User_ID we check directly by it
    # But if api_key is given we firstly need to select user_id by api_key
    if not User_ID and API:
        User_ID = f"""(SELECT User_ID
                       FROM users
                       WHERE API_key='{API}')"""

    # Generate sql to get brain by team and execute
    get_brain_by_team_access_sql = f"""SELECT {properties_to_get_from_braindata}
                                       FROM brains b
                                       INNER JOIN (SELECT ac.Team_ID
                                                   FROM accessright ac
                                                   WHERE ac.User_ID = {User_ID}) teams
                                       ON b.Owner_Team_ID = teams.Team_ID
                                       WHERE b.Brain_ID = {Brain_ID};"""
    brain_object = AI_cursor.execute(get_brain_by_team_access_sql)
    brain_object = [{column: value for column, value in rowproxy.items()} for rowproxy in brain_object]

    # If executed brain_object is empty
    # it means that the user API key doesn't belong
    # to this brain or brain_ID is wrong
    # But we try also to check if user is the owner
    if not brain_object:

        # Generate sql to get brain by owner and execute
        get_brain_by_owner_id = f"""SELECT {properties_to_get_from_braindata}
                                    FROM brains
                                    WHERE Brain_ID = {Brain_ID}
                                    AND Owner_User_ID = {User_ID}"""
        brain_object = AI_cursor.execute(get_brain_by_owner_id)
        brain_object = [{column: value for column, value in rowproxy.items()} for rowproxy in brain_object]

        if not brain_object:
            return None
        else:
            AI_cursor.close()
            return brain_object[0]

    else:
        AI_cursor.close()
        return brain_object[0]


if __name__ == '__main__':

    print(GetBrainIfAuthorized(Brain_ID=2,
                               User_ID=None,
                               API='dcba',
                               for_solve=False))
