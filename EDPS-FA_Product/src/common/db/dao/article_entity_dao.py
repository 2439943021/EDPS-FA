from src.common.db.entity.article_entity import ArticleEntity


class ArticleEntityDao:
    def __init__(self):
        super().__init__()

    def query_article_by_state(self,state ):
        """
        根据状态获取文章
        @param state:
        @param limit:
        @param order_by: 默认根据创建时间 create_time 降序
        @return:
        """
        return ArticleEntity.query(["*"],
                            filter=[
                                ArticleEntity.state == state],
                            limit=1,
                            query_first=True,
                            order_by='create_time')

    def update_article(self, session, update_dict):
        """
        更新文章状态
        @param session: 更新字段类型
        @param update_dict: 更新条件
        @return: 1 代码更新成功 0 代表更新失败
        """
        status = ArticleEntity.update(
            session,
            update_dict)

        return status
