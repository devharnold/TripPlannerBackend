# Workflows State Manager

class WorkflowState:
    def __init__(self):
        self.current_step = None
        self.completed_steps = []
        self.errors = []

    def update_step(self, step: str):
        self.current_step = step
        self.completed__steps.append(step)

    def add_error(self, error: str):
        self.errors.append(error)

    def get_state(self):
        return {
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "errors": self.errors
        }