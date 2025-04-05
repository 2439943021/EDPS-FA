package mapper;

import com.analysis.entity.Article;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.mapstruct.Mapper;

import java.util.List;

/**
 * @author ChenJG
 * @date 2024/3/12 0:11
 */
@Mapper
public interface ArticleMapper extends BaseMapper<Article> {

}
