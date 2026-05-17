from datetime import datetime

class WorkflowState:
    def __init__(self):
        self.current_step = None
        self.completed_steps = []
        self.errors = []
        self.started_at = datetime.utcnow().isoformat()
        self.completed = False

    def update_step(self, step: str):
        self.current_step = step
        self.completed_steps.append(step)

    def add_error(self, error: str):
        self.errors.append(error)

    def mark_completed(self):
        self.completed = True

    def get_state(self):
        return {
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "errors": self.errors,
            "started_at": self.started_at,
            "completed": self.completed
        }