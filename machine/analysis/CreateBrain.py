from sqlalchemy import create_engine
import pandas as pd
import json


"""
LOCATION:       ...
DESCRIPTION:    Create a brain in ai database with pasted parameters and tables in braindata databes with newly created brain_id.
MAIN FUNCTION:  CreateBrain
USAGE:    in main function CreateBrain you pass a dict with properies that should be created in a brain table
    "property_name": value    =>   'ParameterCNN_ShapeAuto': 0
    The function convert this dict into pandas data frame and insert new line in brains DB
    After inserting it returns the inserted ID
    Using this ID number it creates Brain_ID_DataInputLines and Brain_ID_DataOutputLines in braindata DB
"""


def create_connections_to_databases():
    """
    Create connections to databases
    """

    # Information to connect to DB
    port = ***
    host = '***'
    user = '***'
    password = '***'

    # Create database engine
    ai_engine = create_engine("mysql+pymysql://{user}:{pw}@{host}:{port}/{db}"
                              .format(  user = 'root',
                    password = 'ArtSoft2@19',
                    db='ai',
                    host = 'srv102.ixioo.com',
                    port = 3306 
                    ))

    braindata_engine = create_engine("mysql+pymysql://{user}:{pw}@{host}:{port}/{db}"
                              .format(  user = 'root',
                    password = 'ArtSoft2@19',
                    db='braindata',
                    host = 'srv102.ixioo.com',
                    port = 3306 
                    ))


    return ai_engine.connect(), braindata_engine.connect()


AI_cursor, BRAINDATA_cursor = create_connections_to_databases()


def CreateBrain(information_for_creating_brain: dict):

    # Create pandas data frame from dict
    df = pd.DataFrame([information_for_creating_brain])
    # Add this data frame to SQL ai.brains table
    df.to_sql(con=AI_cursor, name='brains', if_exists='append', index=False)
    # Get last inserted id in ai.brains (the one that we insert)
    last_created_brain = AI_cursor.execute('SELECT LAST_INSERT_ID() FROM ai.brains;').fetchone()[0]

    # SQL query for creating a inputlines table in
    # braindata database with our newly created ID
    create_braindata_inputlines_sql = f"""
        CREATE TABLE IF NOT EXISTS `braindata`.`Brain_{last_created_brain}_DataInputLines` (
          `LineInput_ID` INT NOT NULL AUTO_INCREMENT,
          `IsForLearning` BIT(1) NOT NULL DEFAULT 0,
          `IsForSolving` BIT(1) NOT NULL DEFAULT 0,
          `IsWithMissingValues` BIT(1) NOT NULL DEFAULT 0,
          `IsForEvaluation` BIT(1) NOT NULL DEFAULT 0,
          `IsLearned` BIT(1) NOT NULL DEFAULT 0,
          `IsSolved` BIT(1) NOT NULL DEFAULT 0,
        UNIQUE INDEX `LineInput_ID_UNIQUE` (`LineInput_ID` ASC) INVISIBLE,
          INDEX `IsForSolving` (`IsForSolving` ASC) INVISIBLE,
          INDEX `IsForEvaluation` (`IsForEvaluation` ASC) VISIBLE,
          INDEX `IsSolved` (`IsSolved` ASC) VISIBLE,
          INDEX `IsLearned` (`IsLearned` ASC) VISIBLE,
          INDEX `IsForLearning` (`IsForLearning` ASC) VISIBLE,
          INDEX `IsWithMissingValues` (`IsWithMissingValues` ASC) VISIBLE,
        PRIMARY KEY (`LineInput_ID`))
        ENGINE = InnoDB;
"""

    # SQL query for creating a outputlines table in
    # braindata database with our newly created ID
    create_braindata_outputlines_sql = f"""
    CREATE TABLE IF NOT EXISTS `braindata`.`Brain_{last_created_brain}_DataOutputLines` (
     `LineInput_ID` INT NOT NULL,
    PRIMARY KEY (`LineInput_ID`),
    CONSTRAINT `fk_Brain_{last_created_brain}-DataOutputLines_Brain_{last_created_brain}-DataInpu`
    FOREIGN KEY (`LineInput_ID`)
    REFERENCES `braindata`.`Brain_{last_created_brain}_DataInputLines` (`LineInput_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
    ENGINE = InnoDB;
"""
    BRAINDATA_cursor.execute(create_braindata_inputlines_sql)
    BRAINDATA_cursor.execute(create_braindata_outputlines_sql)



if __name__ == '__main__':

    # Test properties
    properties = {
        'Brain_ID_Original': 1,

        'Owner_User_ID': 1,
        'Owner_Team_ID': 1,

        'Project_Name': 'Test',

        'Project_IsPublic': 1,

        'Project_APISolving_IsPublic': 1,

        'AnalysisSource_ColumnsNameInput': json.dumps(["Column18", "Column55", "Column39", "Column16", "Column42", "Column14", "Column5", "Column13", "Column24", "Column45", "Column40", "Column46", "Column12", "Column37", "Column54", "Column20", "Column23", "Column26", "Column3", "Column29", "Column19", "Column59", "Column11", "Column53", "Column15", "Column25", "Column49", "Column51", "Column27", "Column6", "Column43", "Column4", "Column48", "Column10", "Column41", "Column57", "Column44", "Column30", "Column2", "Column33", "Column38", "Column7", "Column17", "Column9", "Column50", "Column58", "Column21", "Column60", "Column47", "Column36", "Column22", "Column56", "Column28", "Column31", "Column32", "Column34", "Column52", "Column8", "Column35", "Column1"]),
        'AnalysisSource_ColumnsNameOutput': json.dumps(["Column61"]),
        'AnalysisSource_ColumnType': json.dumps({"Column1": "NUMERIC", "Column2": "NUMERIC", "Column3": "NUMERIC", "Column4": "NUMERIC", "Column5": "NUMERIC", "Column6": "NUMERIC", "Column7": "NUMERIC", "Column8": "NUMERIC", "Column9": "NUMERIC", "Column10": "NUMERIC", "Column11": "NUMERIC", "Column12": "NUMERIC", "Column13": "NUMERIC", "Column14": "NUMERIC", "Column15": "NUMERIC", "Column16": "NUMERIC", "Column17": "NUMERIC", "Column18": "NUMERIC", "Column19": "NUMERIC", "Column20": "NUMERIC", "Column21": "NUMERIC", "Column22": "NUMERIC", "Column23": "NUMERIC", "Column24": "NUMERIC", "Column25": "NUMERIC", "Column26": "NUMERIC", "Column27": "NUMERIC", "Column28": "NUMERIC", "Column29": "NUMERIC", "Column30": "NUMERIC", "Column31": "NUMERIC", "Column32": "NUMERIC", "Column33": "NUMERIC", "Column34": "NUMERIC", "Column35": "NUMERIC", "Column36": "NUMERIC", "Column37": "NUMERIC", "Column38": "NUMERIC", "Column39": "NUMERIC", "Column40": "NUMERIC", "Column41": "NUMERIC", "Column42": "NUMERIC", "Column43": "NUMERIC", "Column44": "NUMERIC", "Column45": "NUMERIC", "Column46": "NUMERIC", "Column47": "NUMERIC", "Column48": "NUMERIC", "Column49": "NUMERIC", "Column50": "NUMERIC", "Column51": "NUMERIC", "Column52": "NUMERIC", "Column53": "NUMERIC", "Column54": "NUMERIC", "Column55": "NUMERIC", "Column56": "NUMERIC", "Column57": "NUMERIC", "Column58": "NUMERIC", "Column59": "NUMERIC", "Column60": "NUMERIC", "Column61": "LABEL"}),

        'ParameterCNN_ShapeAuto': 0,
        'ParameterCNN_Loss': 'binary_crossentropy',
        'ParameterCNN_Optimizer': 'adam',
        'ParameterCNN_Shape': json.dumps([["", "Dense", "relu"], [60, "Dense", "relu"], ["", "Dense", "sigmoid"]]),
        'ParameterCNN_Epoch': 0,
        'ParameterCNN_BatchSize': 5
    }

    CreateBrain(properties)
