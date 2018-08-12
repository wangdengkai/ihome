#coding:utf-8

'''
这是服务器模块，用户启动网站

'''
import motor
import redis
from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado import web
from urls import urls

from . import config

options.define("port",default=8080,type=int,help="run server ont the given port")

class Application(web.Application):
    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)
        #连接mogodb
        self.client = motor.motor_tornado.MotorClient(config.mongo_options)
        #获取数据库
        self.db = self.client.ihome_db

        #连接redis
        self.redis = redis.StrictRedis(**config.redis_options)


def main():
    options.log_file_prefix = config.log_path
    options.logging  = config.log_level
    # 解析命令行参数
    options.parse_command_line()

    #创建应用
    app = Application(
        urls,
        **config.settings
    )

    #创建http服务器对象
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)

    #启动服务器
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()