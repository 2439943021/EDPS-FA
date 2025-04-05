# dev环境配置
import functools

from src.common.config.config import config

# host = "rm-8vb7w4mo8b6npnet2go.mysql.zhangbei.rds.aliyuncs.com"
# port = 3306
# user = "root"
# database = "ask"
# password = "LWcc123456"
# 连接池大小，默认为5，设置为0时表示连接无限制
pool_size = 10
# 连接池中最大连接数，如果访问数据库的请求数超过了pool_size，连接池将会自动创建新的连接，
# 直到创建达到max_overflow个连接为止。默认情况下，max_overflow值为10
max_overflow = 20
# 连接池中获取连接的等待时间，超过该等待时间后，获取连接方法将会超时，引发连接失败异常。默认情况下，timeout为30秒。
pool_timeout = 60


from sqlalchemy import create_engine

# 数据库连接配置
MYSQL = {
    config.DB_NAME: {
        'user': config.DB_USER,
        'passwd': config.DB_PASSWORD,
        'host': config.DB_HOST,
        'port': config.DB_PORT,
        'db': config.DB_NAME,
    }
}

engines = {}


def init_engines():
    """初始化数据库连接"""
    for k, v in MYSQL.items():
        mysql_url = ("mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}"
                     "?charset=utf8".format(**v))
        engines[k] = create_engine(mysql_url,
                                   pool_size=10,
                                   max_overflow=-1,
                                   pool_recycle=1000,
                                   echo=False)

# 初始化所有数据库的连接，后续如果新增数据库访问，在MYSQL里面直接加入数据库配置即可
init_engines()

from contextlib import contextmanager
from sqlalchemy.orm import scoped_session, sessionmaker

def get_session(db):
    """获取session"""
    return scoped_session(sessionmaker(
        bind=engines[db],
        expire_on_commit=False))()


@contextmanager
def Db_session(db='research', commit=True):
    """db session封装.

    :params db:数据库名称
    :params commit:进行数据库操作后是否进行commit操作的标志
                   True：commit, False:不commit
    """
    session = get_session(db)
    try:
        yield session
        if commit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if session:
            session.close()

def class_dbsession(commit=True):
    """用于BaseModel中进行数据库操作前获取dbsession操作.

    :param commit:进行数据库操作后是否进行commit操作的标志，True：commit, False:不commit
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            # cls为对象或类
            cls = args[0]
            # 实际传入的参数
            new_args = args[1:]
            with Db_session(cls._db_name, commit) as session:
                return func(cls, session, *new_args, **kwargs)
        return inner
    return wrapper