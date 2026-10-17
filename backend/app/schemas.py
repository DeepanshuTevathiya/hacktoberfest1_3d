from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Category(str, Enum):
    appliance = "appliance"; electronics = "electronics"; mechanical = "mechanical"; vehicle = "vehicle"; tool = "tool"; other = "other"


class Template(str, Enum):
    enclosure = "enclosure"; stack = "stack"; radial = "radial"; chain = "chain"; mechanism = "mechanism"


class Shape(str, Enum):
    box = "box"; cylinder = "cylinder"; sphere = "sphere"; cone = "cone"; torus = "torus"; capsule = "capsule"


class Role(str, Enum):
    shell = "shell"; core = "core"; power = "power"; control = "control"; moving = "moving"; sensor = "sensor"; output = "output"; storage = "storage"; connector = "connector"


SLOTS: dict[Template, set[str]] = {
    Template.enclosure: {"shell", "top_left", "top_right", "bottom_left", "bottom_right", "top", "bottom", "left", "right", "center", "front", "back"},
    Template.stack: {f"layer_{i}" for i in range(10)},
    Template.radial: {"center", *{f"ring_{i}" for i in range(9)}},
    Template.chain: {f"step_{i}" for i in range(10)},
    Template.mechanism: {f"r{r}c{c}" for r in range(3) for c in range(3)},
}


class Size(BaseModel):
    w: float = Field(ge=0.2, le=1)
    h: float = Field(ge=0.2, le=1)
    d: float = Field(ge=0.2, le=1)


class Part(BaseModel):
    id: str = Field(pattern=r"^[a-z_]+$")
    name: str = Field(max_length=30)
    shape: Shape
    size: Size
    slot: str
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    role: Role
    hover_text: str = Field(max_length=90)
    fun_fact: str = Field(max_length=140)
    panda_script: str = Field(min_length=1, max_length=300)

    @field_validator("panda_script")
    @classmethod
    def check_words(cls, value: str) -> str:
        if len(value.split()) > 45:
            raise ValueError("panda_script must be 45 words or fewer")
        return value


class Connection(BaseModel):
    from_id: str
    to_id: str
    label: str = Field(max_length=24)


class Blueprint(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    schema_version: int = Field(default=1, frozen=True)
    object_name: str
    slug: str = Field(pattern=r"^[a-z_]+$")
    category: Category
    template: Template
    confidence: float = Field(ge=0, le=1)
    summary: str = Field(max_length=160)
    safety_note: str | None = None
    parts: list[Part] = Field(min_length=4, max_length=10)
    connections: list[Connection] = Field(default_factory=list)
    flow: list[str] = Field(min_length=3, max_length=8)

    @model_validator(mode="after")
    def check_structure(self) -> "Blueprint":
        ids, slots = [p.id for p in self.parts], [p.slot for p in self.parts]
        if len(ids) != len(set(ids)): raise ValueError("part ids must be unique")
        if len(slots) != len(set(slots)): raise ValueError("part slots must be unique")
        invalid = set(slots) - SLOTS[self.template]
        if invalid: raise ValueError(f"invalid slots: {', '.join(sorted(invalid))}")
        shells = [p for p in self.parts if p.role == Role.shell]
        if len(shells) > 1 or (self.template == Template.enclosure and len(shells) != 1):
            raise ValueError("enclosure needs exactly one shell; other templates need at most one")
        if self.template == Template.enclosure and shells[0].slot != "shell": raise ValueError("shell must use shell slot")
        if self.safety_note is not None and not self.safety_note.strip(): raise ValueError("safety_note must not be empty")
        refs = {c.from_id for c in self.connections} | {c.to_id for c in self.connections} | set(self.flow)
        if unknown := refs - set(ids): raise ValueError(f"unknown part ids: {', '.join(sorted(unknown))}")
        return self


class Identification(BaseModel):
    object_name: str
    category: Category
    confidence: float = Field(ge=0, le=1)
    search_query: str
    is_valid_object: bool
