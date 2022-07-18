import json
import os
from os.path import expanduser
from typing import List


class Settings:
    def __init__(self) -> None:
        self.config_name = self.get_config_name()
        self.config_path = self.get_config_path()
        self.full_settings_path = os.path.join(
            self.config_path, self.config_name
        )
        self.create_dir_if_not_exists()

    def get_config_name(self):
        return 'config.json'

    def get_config_path(self):
        return os.path.join(expanduser('~'), '.config', 'pls')

    def get_full_settings_path(self):
        return self.full_settings_path

    def create_dir_if_not_exists(self) -> None:
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)

    def exists_settings(self) -> bool:
        return os.path.exists(self.full_settings_path)

    def get_settings(self) -> dict:
        if os.path.exists(self.full_settings_path):
            with open(
                self.full_settings_path, encoding='utf-8'
            ) as config_file:
                return json.load(config_file)
        return {}

    def write_settings(self, data: dict) -> None:
        with open(
            self.full_settings_path, 'w', encoding='utf-8'
        ) as config_file:
            json.dump(data, config_file, indent=2)

    def get_name(self) -> str:
        return self.get_settings().get('user_name', '')

    def get_tasks(self) -> List[dict]:
        return self.get_settings().get('tasks', [])

    def show_tasks_progress(self) -> bool:
        return self.get_settings().get('show_task_progress', True)

    def show_quotes(self) -> bool:
        return self.get_settings().get('show_quotes', True)

    def all_tasks_done(self) -> bool:
        return all(task.get('done', '') for task in self.get_tasks())

    def get_all_tasks_undone(self) -> List[dict]:
        return [task for task in self.get_tasks() if not task['done']]

    def count_tasks_done(self) -> int:
        if not self.get_tasks():
            return 0
        return len(
            [task.get('done', '') for task in self.get_tasks() if task['done']]
        )

    def count_tasks_undone(self) -> int:
        if not self.get_tasks():
            return 0
        return len(
            [
                task.get('done', '')
                for task in self.get_tasks()
                if not task['done']
            ]
        )
