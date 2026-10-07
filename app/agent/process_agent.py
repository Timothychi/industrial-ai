import json

from app.llm.client import LLMClient
from app.tools.registry import TOOLS, TOOL_DEFINITIONS


class ProcessAgent:

    def __init__(self):

        self.llm = LLMClient()

    async def run(
        self,
        message: str,
    ) -> str:

        messages = [
            {
                "role": "system",
                "content": """
            你是一个工业制造领域的工艺知识助手。

            你的职责：

            1. 帮助用户理解制造工艺。
            2. 查询材料信息。
            3. 查询工业工艺知识。
            4. 综合工具返回的信息回答问题。
            5. 不要编造工具没有提供的数据。

            【知识使用规则】

            如果用户的问题涉及具体的工业参数、
            工艺参数、材料性能、设备能力或标准要求，
            必须优先使用工具查询。

            如果工具返回了相关知识，
            只能基于工具返回的知识回答。

            如果知识库没有找到足够的依据，
            必须明确告诉用户：
            “当前知识库没有找到足够的依据。”

            禁止根据自己的常识编造具体参数、
            数值、标准编号或设备能力。

            【来源规则】

            如果使用了知识库内容，
            回答时尽量说明知识来源。

            例如：

            “根据《车削工艺基础》中的‘45号钢车削’章节……”

            如果不同知识来源之间存在冲突，
            不要自行判断哪个一定正确，
            应该指出存在冲突，并展示来源。
            """
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        while True:

            response = await self.llm.chat(
                messages=messages,
                tools=TOOL_DEFINITIONS,
            )

            assistant_message = response[
                "choices"
            ][0]["message"]

            messages.append(
                assistant_message
            )

            tool_calls = assistant_message.get(
                "tool_calls"
            )

            # 没有 Tool 调用
            if not tool_calls:

                return assistant_message[
                    "content"
                ]

            # 执行所有 Tool
            for tool_call in tool_calls:

                function_name = (
                    tool_call["function"]["name"]
                )

                arguments = json.loads(
                    tool_call["function"]["arguments"]
                )

                tool = TOOLS.get(
                    function_name
                )

                if tool is None:

                    raise ValueError(
                        f"Tool 不存在: {function_name}"
                    )

                result = tool(
                    **arguments
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": json.dumps(
                            result,
                            ensure_ascii=False,
                        ),
                    }
                )