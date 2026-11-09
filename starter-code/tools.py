import json
import os
from typing import List, Dict, Any
from datetime import datetime

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "raw-data")

# ---------------------------------------------------------------------------
# Tool #1: search_product_catalog
# TODO: Hoàn thiện hàm này — đọc file product_catalog.json, lọc theo category và max_price.
# ---------------------------------------------------------------------------

def search_product_catalog(category: str, max_price: int = 999999999999) -> List[Dict[str, Any]]:
    """
    Tra cứu sản phẩm/dịch vụ Vingroup theo danh mục và giá tối đa.
    
    Args:
        category: Loại sản phẩm ('xe_dien' hoặc 'du_lich').
        max_price: Giá tối đa (VNĐ). Mặc định không giới hạn.
    
    Returns:
        Danh sách sản phẩm phù hợp điều kiện.
    """
    catalog_file = os.path.join(RAW_DATA_DIR, "product_catalog.json")
    if not os.path.exists(catalog_file):
        return [("error", "File product_catalog.json không tồn tại.")]
    
    with open(catalog_file, "r", encoding="utf-8") as f:
        try:
            products = json.load(f)
        except json.JSONDecodeError:
            return [("error", "File product_catalog.json không hợp lệ.")]
    results = [
        p for p in products if p.get("category") == category and p.get("price_vnd", 0) <= max_price 
    ]
    # TODO: Kiểm tra file tồn tại, đọc JSON, lọc sản phẩm
    # Gợi ý: Lọc theo p["category"] == category AND p["price_vnd"] <= max_price
    return results


# ---------------------------------------------------------------------------
# Tool #2: submit_support_ticket
# TODO: Hoàn thiện hàm này — tạo ticket mới và lưu vào support_tickets.json.
# ---------------------------------------------------------------------------

def submit_support_ticket(
    customer_name: str,
    issue_description: str,
    priority: str = "medium") -> Dict[str, Any]:
    """
    Ghi nhận yêu cầu hỗ trợ của khách hàng vào hệ thống ticket.
    
    Args:
        customer_name: Tên khách hàng.
        issue_description: Mô tả vấn đề cần hỗ trợ.
        priority: Mức độ ưu tiên ('low', 'medium', 'high'). Mặc định 'medium'.
    
    Returns:
        Thông tin ticket vừa tạo bao gồm ticket_id, status.
    """
    tickets_file = os.path.join(RAW_DATA_DIR, "support_tickets.json")

    #Load existing tickets if the file exists
    existing_tickets = []
    if os.path.exists(tickets_file):
        with open(tickets_file, "r", encoding="utf-8") as f:
            existing_tickets = json.load(f)

    #Generate new ticket_id
    today = datetime.now().strftime("%Y%m%d")
    seq = len(existing_tickets) + 1
    ticket_id = f"TK-{today}-{seq:3d}"

    new_ticket = {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "issue_description": issue_description,
        "priority": priority.lower(),
        "status": "open",
        "created_at": datetime.now().isoformat() + "+07:00",
        "category": "general"
    }

    #Append new ticket to existing tickets
    existing_tickets.append(new_ticket)

    #Persist the updated tickets list back to the JSON file
    with open(tickets_file, "w", encoding="utf-8") as f:
        json.dump(existing_tickets, f, ensure_ascii=False, indent=2)
    


    # TODO: Load existing tickets, generate new ticket_id, append new ticket, save file
    # Gợi ý: ticket_id = f"TK-{today}-{seq:03d}" với today = datetime.now().strftime("%Y%m%d")
    return {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "priority": priority.lower(),
        "status": "open",
        "message": f"Ticket {ticket_id} đã được tạo thành công cho khách hàng {customer_name}."
    }



# ---------------------------------------------------------------------------
# TOOL_DEFINITIONS — JSON Schemas mô tả cho LLM
# TODO: Định nghĩa JSON Schema cho từng tool (name, description, parameters).
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    # TODO: Thêm schema cho "search_product_catalog"
    {
        "name": "search_product_catalog",
        "description": "Tra cứu sản phẩm/dịch vụ Vingroup (xe điện VinFast, resort Vinpearl) theo danh mục và giá tối đa.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Loại sản phẩm: 'xe_dien' cho xe điện VinFast, 'du_lich' cho gói du lịch Vinpearl.",
                    "enum": ["xe_dien", "du_lich"]
                },
                "max_price": {
                    "type": "integer",
                    "description": "Giá tối đa tính bằng VNĐ. Ví dụ: 600000000 cho 600 triệu."
                }
            },
            "required": ["category"]
        }
    },

    # TODO: Thêm schema cho "submit_support_ticket"
    {
        "name": "submit_support_ticket",
        "description": "Ghi nhận yêu cầu hỗ trợ khách hàng vào hệ thống ticket. Dùng khi khách hàng phản ánh lỗi, khiếu nại hoặc cần trợ giúp.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_name": {
                    "type": "string",
                    "description": "Họ tên đầy đủ của khách hàng."
                },
                "issue_description": {
                    "type": "string",
                    "description": "Mô tả chi tiết vấn đề khách hàng gặp phải."
                },
                "priority": {
                    "type": "string",
                    "description": "Mức độ ưu tiên: 'low' (thấp), 'medium' (trung bình), 'high' (cao/khẩn cấp).",
                    "enum": ["low", "medium", "high"],
                    "default": "medium"
                }
            },
            "required": ["customer_name", "issue_description"]
        }
    }


]


# ---------------------------------------------------------------------------
# TOOL_MAP — Ánh xạ tên tool → hàm thực thi
# ---------------------------------------------------------------------------

TOOL_MAP = {
    "search_product_catalog": search_product_catalog,
    "submit_support_ticket": submit_support_ticket
}
