from pydantic import BaseModel
from model.task import Task

class Area(BaseModel):
  name: str
  tasks: list[Task]

  def add_task(self, task: Task):
    self.tasks.append(task)

  def str_tasks(self, indent=''):
    return '\n'.join([task.__str__(indent) for task in self.tasks])

  def __str__(self):
    return f'''Area: {{
  Name: {self.tasks[0].area_name},
  Tasks: [
{self.str_tasks(indent='    ')} 
  ]
}}'''
