import workflow


class PlanBuilder:
    def __init__(self, saved_state=workflow.flow["build_plan"]):
        self.flow = workflow.flow["build_plan"]
        self.current_state = saved_state["init"]
        self.title = saved_state["title"]
        self.suggests = saved_state["suggests"]

    def process_step(self, data):
        result = {}
        getattr(self, self.current_state)(data)
        result["suggests"] = self.suggests
        return result
