# 个人信息管理 MCP 工具

这是一个简单的 MCP (Model Context Protocol) 工具，用于管理个人基本信息，包括姓名、出生时间和地点信息。

## 功能特性

- **添加个人信息**: 存储姓名、性别、出生时间（年月日时分）、地点（城市名及经纬度）和时区信息
- **查询个人信息**: 根据姓名查询已存储的信息
- **列出所有信息**: 显示所有已存储的个人信息
- **更新个人信息**: 选择性更新已存储的信息字段
- **删除个人信息**: 根据姓名删除信息

## 文件结构

```
/Users/wuguangxin/Documents/个人工具/MCPDocument/
├── person_info_mcp.py    # 主程序文件
├── mcp_config.json       # MCP 配置文件
├── README.md            # 说明文档
└── person_data.json     # 数据存储文件（运行后自动生成）
```

## 数据格式

每个人的信息包含以下字段：

```json
{
  "name": "张三",
  "gender": "男",
  "birth_time": {
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "datetime_str": "1990-05-15 14:30"
  },
  "location": {
    "city": "北京",
    "latitude": 39.9042,
    "longitude": 116.4074
  },
  "timezone": "Asia/Shanghai",
  "created_at": "2024-01-15 10:30:00",
  "updated_at": "2024-01-15 11:00:00"
}
```

## 可用工具

### 1. add_person
添加新的个人信息

**参数:**
- `name` (string): 姓名
- `birth_year` (integer): 出生年份
- `birth_month` (integer): 出生月份 (1-12)
- `birth_day` (integer): 出生日期 (1-31)
- `birth_hour` (integer): 出生小时 (0-23)
- `birth_minute` (integer): 出生分钟 (0-59)
- `city` (string): 出生城市
- `latitude` (number): 纬度 (-90 到 90)
- `longitude` (number): 经度 (-180 到 180)
- `gender` (string, 可选): 性别
- `timezone` (string, 可选): 时区（如：Asia/Shanghai, UTC+8等）

### 2. get_person
根据姓名查询个人信息

**参数:**
- `name` (string): 要查询的姓名

### 3. list_all_persons
列出所有已存储的个人信息

**参数:** 无

### 4. update_person
更新个人信息（可选择性更新字段）

**参数:**
- `name` (string): 要更新的姓名（必需）
- `birth_year` (integer, 可选): 出生年份
- `birth_month` (integer, 可选): 出生月份
- `birth_day` (integer, 可选): 出生日期
- `birth_hour` (integer, 可选): 出生小时
- `birth_minute` (integer, 可选): 出生分钟
- `city` (string, 可选): 出生城市
- `latitude` (number, 可选): 纬度
- `longitude` (number, 可选): 经度
- `gender` (string, 可选): 性别
- `timezone` (string, 可选): 时区

### 5. delete_person
根据姓名删除个人信息

**参数:**
- `name` (string): 要删除的姓名

## 使用方法

1. 确保已安装 Python 3.6+
2. 将 `mcp_config.json` 中的路径配置到你的 MCP 客户端
3. 启动 MCP 服务器：
   ```bash
   python3 person_info_mcp.py
   ```

## 数据验证

- 姓名不能为空且不能重复
- 日期时间必须是有效的日期
- 纬度范围：-90 到 90
- 经度范围：-180 到 180

## 错误处理

工具会返回详细的错误信息，包括：
- 数据验证错误
- 文件读写错误
- 重复姓名错误
- 未找到记录错误

## 时区支持

系统支持标准时区格式，常用时区包括：
- `Asia/Shanghai` - 中国标准时间 (UTC+8)
- `Asia/Taipei` - 台湾时间 (UTC+8)
- `Asia/Seoul` - 韩国标准时间 (UTC+9)
- `UTC` - 协调世界时
- `America/New_York` - 美国东部时间
- `Europe/London` - 英国时间

## 注意事项

- 数据以 JSON 格式存储在本地文件中
- 姓名作为唯一标识符，不允许重复
- 时区信息采用标准 IANA 时区数据库格式
- 性别和时区字段为可选，向后兼容现有数据
- 建议定期备份 `person_data.json` 文件