# 个人信息管理 MCP 工具

这是一个简单的 MCP (Model Context Protocol) 工具，用于管理个人基本信息，包括姓名、出生时间和地点信息。

## 功能特性

- **添加个人信息**: 存储姓名、性别、出生时间（年月日时分）、地点（城市名及经纬度）和时区信息
- **查询个人信息**: 根据姓名查询已存储的信息
- **模糊搜索**: 支持中文和拼音的智能模糊搜索，包括前两个字匹配、后两个字匹配等
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

### 3. search_persons
模糊搜索个人信息，支持中文和拼音匹配

**参数:**
- `query` (string): 搜索关键词（至少2个字符）
- `search_type` (string, 可选): 搜索类型（默认为"fuzzy"）

**搜索特性:**
- **中文匹配**: 前两个字匹配、后两个字匹配、包含匹配
- **拼音匹配**: 拼音前两个字匹配、拼音后两个字匹配、拼音包含匹配
- **智能排序**: 按匹配分数自动排序，最相关结果优先显示
- **不区分大小写**: 拼音搜索自动转换为小写进行匹配

### 4. list_all_persons
列出所有已存储的个人信息

**参数:** 无

### 5. update_person
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

### 6. delete_person
根据姓名删除个人信息

**参数:**
- `name` (string): 要删除的姓名

## 使用方法

1. 确保已安装 Python 3.6+
2. 安装必要的依赖：
   ```bash
   pip3 install pypinyin
   ```
3. 将 `mcp_config.json` 中的路径配置到你的 MCP 客户端
4. 启动 MCP 服务器：
   ```bash
   python3 person_info_mcp.py
   ```

## 数据验证

- 姓名不能为空且不能重复
- 日期时间必须是有效的日期
- 纬度范围：-90 到 90
- 经度范围：-180 到 180
- 搜索关键词至少需要2个字符

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

## 搜索功能详解

### 中文匹配模式
- **前两个字匹配**: 输入"张三"匹配所有以"张三"开头的姓名
- **后两个字匹配**: 输入"小明"匹配所有以"小明"结尾的姓名
- **包含匹配**: 输入"张"匹配所有包含"张"的姓名

### 拼音匹配模式
- **拼音前两个字匹配**: 输入"zhang"匹配所有以"zhang"开头的姓名拼音
- **拼音后两个字匹配**: 输入"si"匹配所有以"si"结尾的姓名拼音
- **拼音包含匹配**: 输入"zh"匹配所有包含该拼音片段的姓名

### 匹配优先级
1. 前两个字匹配 (100分)
2. 拼音前两个字匹配 (95分)
3. 后两个字匹配 (80分)
4. 拼音后两个字匹配 (75分)
5. 包含匹配 (60分)
6. 拼音包含匹配 (55分)

### 额外加分规则
- 完全匹配: +20分
- 长度匹配: +10分（姓名长度与查询长度相同）

## 注意事项

- 数据以 JSON 格式存储在本地文件中
- 姓名作为唯一标识符，不允许重复
- 时区信息采用标准 IANA 时区数据库格式
- 性别和时区字段为可选，向后兼容现有数据
- 拼音搜索需要安装 `pypinyin` 库
- 建议定期备份 `person_data.json` 文件