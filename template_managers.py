import json
import pathlib
from random import choice
from typing import List, Dict, Optional, Union

from pydantic import BaseModel, Field


class CpTemplateManager(BaseModel):
    class Config:
        allow_mutation = False
        validate_assignment = True

    template_file_path: str = Field(exclude=True)
    attack_match_string: str = Field(default="<攻>", exclude=True)
    defense_match_string: str = Field(default="<受>", exclude=True)
    templates: List[str] = Field(default_factory=list, const=True, unique_items=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.load()
        self.validate_templates()

    def validate_templates(self) -> bool:
        pass_verify = True
        for template in self.templates:
            template: str
            if not (self.attack_match_string in template and self.defense_match_string in template):
                self.templates.remove(template)
                pass_verify = False

        return pass_verify

    def make_meme_string(self, attack: str, defense: str, index: Optional[int] = None) -> str:
        if index:
            try:
                result_string = self.templates[index]
            except IndexError:
                result_string = choice(self.templates)
        else:
            result_string = choice(self.templates)

        result_string = result_string.replace(self.attack_match_string, attack)
        result_string = result_string.replace(self.defense_match_string, defense)
        return result_string

    def save(self):
        pathlib.Path(self.template_file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.template_file_path, "w", encoding="utf-8") as f:
            json.dump(self.dict(), f, indent=2, ensure_ascii=False)

    def load(self):
        self.templates.clear()
        with open(self.template_file_path, "r", encoding="utf-8") as f:
            data: Dict[str, List] = json.load(f)
            templates = data.get("templates", [])
            self.templates.extend(templates)

    def add_template(self, new_template: str, with_save=True) -> bool:
        self.templates.append(new_template)
        success = self.validate_templates()
        self.save() if with_save else None
        return success

    def remove_template(self, target: Union[str, int], with_save=True) -> bool:
        success = False
        try:
            self.templates.pop(target) if isinstance(target, int) else self.templates.remove(target)
            success = True
        except IndexError:
            pass
        except ValueError:
            pass

        self.save() if with_save else None
        return success
