from src.common.config.config import config

from qiniu import Auth, put_file, etag


def upload_file(file_path,upload_path):
    """
    oss 上传文件
    @param file_path: 文件原始路径
    @param upload_path: 上传后的文件路径 组成由前缀+文件名 如pdf 存放在pdf路径 于是为pdf/文件名 报告则为render/文件名
    @return:
    """
    access_key = config.OSS_QINIU_ACCESS_KEY
    secret_key = config.OSS_QINIU_SECRET_KEY
    q = Auth(access_key, secret_key)
    bucket_name = config.OSS_QINIU_BUCKET_NAME
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, upload_path, 3600)

    # 要上传文件的本地路径
    ret, info = put_file(token, upload_path, file_path, version='v2')
    # print(info)
    return config.OSS_QINIU_BUCKET_DOMAIN + upload_path


if __name__ == "__main__":
    upload_file(
        r'E:\HUTYGTEAM\ASK\Autovalseeker\pdfs\36228738_Monogenic_early-onset_lymphoproliferation_and_autoimmunity_Natural_history_of_STAT3_gain-of-function_syndrome.pdf')
