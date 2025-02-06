### FastAPI RESTful API服务

#### 项目概述
本项目是一个基于FastAPI的RESTful API服务，提供了用户管理和物品管理的功能。通过集成CORS中间件，允许跨域请求，并且在应用启动时会自动创建数据库表结构。

#### 目录结构
```
FastAPI-RESTful-API/
├── main.py             # FastAPI应用入口文件
├── core/
│   ├── config.py       # 应用配置项
│   ├── database.py     # 数据库相关操作
│   ├── exceptions.py   # 错误处理逻辑
│   └── logging.py      # 日志记录配置
├── models/
│   ├── __init__.py     # 初始化文件
│   ├── user.py         # 用户模型
│   └── item.py         # 物品模型
├── routers/
│   ├── __init__.py     # 初始化文件
│   ├── user.py         # 用户管理路由
│   └── item.py         # 物品管理路由
├── services/
│   ├── __init__.py     # 初始化文件
│   ├── user.py         # 用户服务逻辑
│   └── item.py         # 物品服务逻辑
└── utils/
    └── dependencies.py # 依赖注入工具
```

#### 环境依赖
确保已安装Python 3.7+版本，并使用pip安装以下依赖：
```bash
pip install fastapi uvicorn sqlalchemy databases[sqlite] sqlmodel python-multipart
```

#### 配置说明
- `core/config.py` 中定义了应用的基本配置项，如应用标题、版本号和端口号等。
- 数据库连接字符串等敏感信息建议通过环境变量或配置文件进行管理。

#### 启动服务
1. 在命令行中进入项目根目录。
2. 运行以下命令启动服务：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port <你的端口号>
```
> 注意：请根据实际情况替换 `<你的端口号>` 为具体值。

#### API文档
启动服务后，可以通过浏览器访问 [http://localhost:<你的端口号>/docs](http://localhost:<你的端口号>/docs) 查看自动生成的交互式API文档。

#### 数据库初始化
- 应用启动时会自动调用 `create_db_and_tables()` 函数来创建所需的数据库表结构。
- 如果需要手动初始化数据库，可以在 `core/database.py` 中实现具体的数据库初始化逻辑。

#### 中间件
- 使用了 `CORSMiddleware` 来处理跨域资源共享问题，默认允许所有来源、凭证、方法和头部的请求。

#### 路由模块
- **用户管理**：提供用户相关的增删改查接口，前缀为 `/users`。
- **物品管理**：提供物品相关的增删改查接口，前缀为 `/items`。

#### 日志记录
- 使用 `core/logging.py` 中配置的日志记录器，在应用启动和关闭时输出相应的日志信息。

#### 开发与调试
- 使用 `--reload` 参数可以让Uvicorn在代码发生变化时自动重启服务器，方便开发调试。
- 建议在开发环境中开启调试模式，以便更好地定位问题。

#### 测试
- 可以通过编写单元测试来验证各个接口的功能是否正常。
- 推荐使用 `pytest` 或其他测试框架来进行自动化测试。

---

如有任何疑问或建议，请随时联系开发者团队。感谢您的支持！