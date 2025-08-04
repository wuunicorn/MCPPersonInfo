#!/usr/bin/env python3
"""
个人信息管理 MCP 工具
支持存储个人姓名、出生时间（年月日时分）以及地点（城市名及经纬度）
支持增删改查操作
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# 数据存储文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), "person_data.json")


class PersonInfoManager:
    """个人信息管理类"""
    
    def __init__(self):
        self.data_file = DATA_FILE
        self.persons = self._load_data()
    
    def _load_data(self) -> Dict:
        """从文件加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"加载数据错误: {e}", file=sys.stderr)
            return {}
    
    def _save_data(self) -> bool:
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.persons, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据错误: {e}", file=sys.stderr)
            return False
    
    def add_person(self, name: str, birth_year: int, birth_month: int, birth_day: int, 
                   birth_hour: int, birth_minute: int, city: str, latitude: float, longitude: float, gender: str = None, timezone: str = None) -> Dict:
        """添加个人信息"""
        try:
            # 验证数据
            if not name or name.strip() == "":
                return {"success": False, "error": "姓名不能为空"}
            
            if name in self.persons:
                return {"success": False, "error": f"姓名 '{name}' 已存在"}
            
            # 验证日期
            try:
                datetime(birth_year, birth_month, birth_day, birth_hour, birth_minute)
            except ValueError as e:
                return {"success": False, "error": f"日期时间格式错误: {e}"}
            
            # 验证经纬度
            if not (-90 <= latitude <= 90):
                return {"success": False, "error": "纬度必须在-90到90之间"}
            if not (-180 <= longitude <= 180):
                return {"success": False, "error": "经度必须在-180到180之间"}
            
            # 添加数据
            person_info = {
                "name": name,
                "birth_time": {
                    "year": birth_year,
                    "month": birth_month,
                    "day": birth_day,
                    "hour": birth_hour,
                    "minute": birth_minute,
                    "datetime_str": f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d} {birth_hour:02d}:{birth_minute:02d}"
                },
                "location": {
                    "city": city,
                    "latitude": latitude,
                    "longitude": longitude
                },
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 添加性别信息（如果提供）
            if gender:
                person_info["gender"] = gender
            
            # 添加时区信息（如果提供）
            if timezone:
                person_info["timezone"] = timezone
            
            self.persons[name] = person_info
            
            if self._save_data():
                return {"success": True, "data": person_info, "message": f"成功添加 '{name}' 的信息"}
            else:
                return {"success": False, "error": "保存数据失败"}
                
        except Exception as e:
            return {"success": False, "error": f"添加失败: {str(e)}"}
    
    def get_person(self, name: str) -> Dict:
        """查询个人信息"""
        try:
            if name in self.persons:
                return {"success": True, "data": self.persons[name]}
            else:
                return {"success": False, "error": f"未找到姓名为 '{name}' 的信息"}
        except Exception as e:
            return {"success": False, "error": f"查询失败: {str(e)}"}
    
    def list_all_persons(self) -> Dict:
        """列出所有个人信息"""
        try:
            if not self.persons:
                return {"success": True, "data": [], "message": "暂无数据"}
            
            persons_list = list(self.persons.values())
            return {
                "success": True, 
                "data": persons_list, 
                "count": len(persons_list),
                "message": f"共找到 {len(persons_list)} 条记录"
            }
        except Exception as e:
            return {"success": False, "error": f"查询失败: {str(e)}"}
    
    def update_person(self, name: str, **kwargs) -> Dict:
        """更新个人信息"""
        try:
            if name not in self.persons:
                return {"success": False, "error": f"未找到姓名为 '{name}' 的信息"}
            
            person = self.persons[name]
            updated = False
            
            # 更新出生时间
            if any(k in kwargs for k in ['birth_year', 'birth_month', 'birth_day', 'birth_hour', 'birth_minute']):
                birth_time = person['birth_time'].copy()
                if 'birth_year' in kwargs:
                    birth_time['year'] = kwargs['birth_year']
                if 'birth_month' in kwargs:
                    birth_time['month'] = kwargs['birth_month']
                if 'birth_day' in kwargs:
                    birth_time['day'] = kwargs['birth_day']
                if 'birth_hour' in kwargs:
                    birth_time['hour'] = kwargs['birth_hour']
                if 'birth_minute' in kwargs:
                    birth_time['minute'] = kwargs['birth_minute']
                
                # 验证新的日期时间
                try:
                    datetime(birth_time['year'], birth_time['month'], birth_time['day'], 
                           birth_time['hour'], birth_time['minute'])
                    birth_time['datetime_str'] = f"{birth_time['year']:04d}-{birth_time['month']:02d}-{birth_time['day']:02d} {birth_time['hour']:02d}:{birth_time['minute']:02d}"
                    person['birth_time'] = birth_time
                    updated = True
                except ValueError as e:
                    return {"success": False, "error": f"日期时间格式错误: {e}"}
            
            # 更新地点信息
            if any(k in kwargs for k in ['city', 'latitude', 'longitude']):
                location = person['location'].copy()
                if 'city' in kwargs:
                    location['city'] = kwargs['city']
                if 'latitude' in kwargs:
                    if not (-90 <= kwargs['latitude'] <= 90):
                        return {"success": False, "error": "纬度必须在-90到90之间"}
                    location['latitude'] = kwargs['latitude']
                if 'longitude' in kwargs:
                    if not (-180 <= kwargs['longitude'] <= 180):
                        return {"success": False, "error": "经度必须在-180到180之间"}
                    location['longitude'] = kwargs['longitude']
                
                person['location'] = location
                updated = True
            
            # 更新性别信息
            if 'gender' in kwargs:
                person['gender'] = kwargs['gender']
                updated = True
            
            # 更新时区信息
            if 'timezone' in kwargs:
                person['timezone'] = kwargs['timezone']
                updated = True
            
            if not updated:
                return {"success": False, "error": "没有提供需要更新的字段"}
            
            person['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if self._save_data():
                return {"success": True, "data": person, "message": f"成功更新 '{name}' 的信息"}
            else:
                return {"success": False, "error": "保存数据失败"}
                
        except Exception as e:
            return {"success": False, "error": f"更新失败: {str(e)}"}
    
    def delete_person(self, name: str) -> Dict:
        """删除个人信息"""
        try:
            if name not in self.persons:
                return {"success": False, "error": f"未找到姓名为 '{name}' 的信息"}
            
            deleted_person = self.persons.pop(name)
            
            if self._save_data():
                return {"success": True, "data": deleted_person, "message": f"成功删除 '{name}' 的信息"}
            else:
                # 如果保存失败，恢复数据
                self.persons[name] = deleted_person
                return {"success": False, "error": "保存数据失败"}
                
        except Exception as e:
            return {"success": False, "error": f"删除失败: {str(e)}"}


# 全局管理器实例
manager = PersonInfoManager()


def main():
    """主函数 - 处理 MCP 请求"""
    
    # 读取标准输入
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "initialize":
                # 初始化响应
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "person-info-mcp-server",
                            "version": "1.0.0",
                            "description": "个人信息管理服务器 - 支持增删改查个人基本信息"
                        }
                    }
                }
            
            elif method == "tools/list":
                # 返回可用工具列表
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "add_person",
                                "description": "添加个人信息，包括姓名、出生时间、地点、性别和时区",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "description": "姓名"},
                                        "birth_year": {"type": "integer", "description": "出生年份"},
                                        "birth_month": {"type": "integer", "description": "出生月份 (1-12)"},
                                        "birth_day": {"type": "integer", "description": "出生日期 (1-31)"},
                                        "birth_hour": {"type": "integer", "description": "出生小时 (0-23)"},
                                        "birth_minute": {"type": "integer", "description": "出生分钟 (0-59)"},
                                        "city": {"type": "string", "description": "出生城市"},
                                        "latitude": {"type": "number", "description": "纬度 (-90 到 90)"},
                                        "longitude": {"type": "number", "description": "经度 (-180 到 180)"},
                                        "gender": {"type": "string", "description": "性别（可选）"},
                                        "timezone": {"type": "string", "description": "时区（可选，如：Asia/Shanghai, UTC+8等）"}
                                    },
                                    "required": ["name", "birth_year", "birth_month", "birth_day", "birth_hour", "birth_minute", "city", "latitude", "longitude"]
                                }
                            },
                            {
                                "name": "get_person",
                                "description": "根据姓名查询个人信息",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "description": "要查询的姓名"}
                                    },
                                    "required": ["name"]
                                }
                            },
                            {
                                "name": "list_all_persons",
                                "description": "列出所有已存储的个人信息",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {},
                                    "required": []
                                }
                            },
                            {
                                "name": "update_person",
                                "description": "更新个人信息（可选择性更新字段）",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "description": "要更新的姓名"},
                                        "birth_year": {"type": "integer", "description": "出生年份（可选）"},
                                        "birth_month": {"type": "integer", "description": "出生月份（可选）"},
                                        "birth_day": {"type": "integer", "description": "出生日期（可选）"},
                                        "birth_hour": {"type": "integer", "description": "出生小时（可选）"},
                                        "birth_minute": {"type": "integer", "description": "出生分钟（可选）"},
                                        "city": {"type": "string", "description": "出生城市（可选）"},
                                        "latitude": {"type": "number", "description": "纬度（可选）"},
                                        "longitude": {"type": "number", "description": "经度（可选）"},
                                        "gender": {"type": "string", "description": "性别（可选）"},
                                        "timezone": {"type": "string", "description": "时区（可选，如：Asia/Shanghai, UTC+8等）"}
                                    },
                                    "required": ["name"]
                                }
                            },
                            {
                                "name": "delete_person",
                                "description": "根据姓名删除个人信息",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "description": "要删除的姓名"}
                                    },
                                    "required": ["name"]
                                }
                            }
                        ]
                    }
                }
            
            elif method == "tools/call":
                # 处理工具调用
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "add_person":
                    result = manager.add_person(
                        arguments.get("name"),
                        arguments.get("birth_year"),
                        arguments.get("birth_month"),
                        arguments.get("birth_day"),
                        arguments.get("birth_hour"),
                        arguments.get("birth_minute"),
                        arguments.get("city"),
                        arguments.get("latitude"),
                        arguments.get("longitude"),
                        arguments.get("gender"),
                        arguments.get("timezone")
                    )
                    
                elif tool_name == "get_person":
                    result = manager.get_person(arguments.get("name"))
                    
                elif tool_name == "list_all_persons":
                    result = manager.list_all_persons()
                    
                elif tool_name == "update_person":
                    name = arguments.pop("name", None)
                    if name:
                        result = manager.update_person(name, **arguments)
                    else:
                        result = {"success": False, "error": "缺少姓名参数"}
                        
                elif tool_name == "delete_person":
                    result = manager.delete_person(arguments.get("name"))
                    
                else:
                    result = {"success": False, "error": f"未知工具: {tool_name}"}
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                        "isError": not result.get("success", False)
                    }
                }
            
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": "Method not found"}
                }
            
            # 输出响应
            print(json.dumps(response, ensure_ascii=False))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }, ensure_ascii=False))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }, ensure_ascii=False))
            sys.stdout.flush()


if __name__ == "__main__":
    main()