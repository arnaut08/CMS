import pymysql
import config.configurations as config

#Database connection object
connection = pymysql.connect(
    host=config.HOST,
    user=config.USER,
    password=config.PASSWORD,
    db=config.DATABASE,
    charset=config.CHARSET,
    connect_timeout=config.TIMEOUT,
    cursorclass=pymysql.cursors.DictCursor
    )