from sqlalchemy.dialects.postgresql import TSVECTOR, TEXT, INTEGER, REAL
from sqlalchemy.sql.expression import case
from sqlalchemy.schema import MetaData
from sqlalchemy import func, select, union_all, text, literal, and_
import pandas as pd
import re
import os
from project.PROJECT_sql_common import PROJECT_Tables


def PROJECT_data(pkid):
    sql_user = os.environ.get('POSTGRES_USER')
    sql_pass = os.environ.get('POSTGRES_PASSWORD')
    
    # sqlalchemy interface object with db
    tab = PROJECT_Tables(sql_user, sql_pass)
    result = list(tab.execute(
                tab.example_table.select().where(
                         tab.member_table.c.pkid == pkid)))
    return result
