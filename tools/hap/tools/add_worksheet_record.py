import json
from typing import Any, Generator
import httpx
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool


class AddWorksheetRecordTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        appkey = tool_parameters.get("appkey", "")
        if not appkey:
            yield self.create_text_message("Invalid parameter App Key")
        sign = tool_parameters.get("sign", "")
        if not sign:
            yield self.create_text_message("Invalid parameter Sign")
        worksheet_id = tool_parameters.get("worksheet_id", "")
        if not worksheet_id:
            yield self.create_text_message("Invalid parameter Worksheet ID")
        record_data = tool_parameters.get("record_data", "")
        if not record_data:
            yield self.create_text_message("Invalid parameter Record Row Data")
        host = tool_parameters.get("host", "")
        if not host:
            host = "https://api.mingdao.com"
        elif not host.startswith(("http://", "https://")):
            yield self.create_text_message("Invalid parameter Host Address")
        else:
            host = f"{host.removesuffix('/')}/api"
        url = f"{host}/v2/open/worksheet/addRow"
        headers = {"Content-Type": "application/json"}
        payload = {"appKey": appkey, "sign": sign, "worksheetId": worksheet_id}
        try:
            payload["controls"] = json.loads(record_data)
            res = httpx.post(url, headers=headers, json=payload, timeout=60)
            res.raise_for_status()
            res_json = res.json()
            if res_json.get("error_code") != 1:
                yield self.create_text_message(f"Failed to add the new record. {res_json['error_msg']}")
            yield self.create_text_message(f"New record added successfully. The record ID is {res_json['data']}.")
        except httpx.RequestError as e:
            yield self.create_text_message(f"Failed to add the new record, request error: {e}")
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"Failed to parse JSON response: {e}")
        except Exception as e:
            yield self.create_text_message(f"Failed to add the new record, unexpected error: {e}")
