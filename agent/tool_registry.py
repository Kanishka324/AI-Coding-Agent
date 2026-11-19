
class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register_tool(self, name, description, function, parameters):
        self.tools[name] = {
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters
        }

    def get_tool_declarations(self):
        declarations = []

        for tool in self.tools.values():
            declarations.append({
                "type": "function",
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            })

        return declarations

    def execute_tool(self, name, arguments):
        tool = self.tools.get(name)

        if tool is None:
            return {
                "success": False,
                "error": f"Tool '{name}' is not registered."
            }

        try:
            result = tool["function"](**arguments)

            return {
                "success": True,
                "result": result
            }

        except Exception as error:
            return {
                "success": False,
                "error": str(error)
            }
