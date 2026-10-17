import json
import re
from io import BytesIO
from PIL import Image
from .cache import BlueprintCache
from .demo import microwave, television
from .schemas import Blueprint, Category, Identification
from .providers.gemma import GemmaProvider


def slugify(value: str) -> str:
    return re.sub(r"[^a-z_]+", "_", value.lower().replace(" ", "_")).strip("_") or "unknown_object"


def shrink_image(raw: bytes) -> bytes:
    image = Image.open(BytesIO(raw)); image.thumbnail((768, 768))
    output = BytesIO(); image.convert("RGB").save(output, format="JPEG", quality=78, optimize=True)
    return output.getvalue()


def fallback_blueprint(name: str, category: Category = Category.other) -> Blueprint:
    slug = slugify(name)
    # A calm generic model means the experience remains explorable when a provider is unavailable.
    return Blueprint.model_validate({"schema_version":1,"object_name":name.title(),"slug":slug,"category":category,"template":"enclosure","confidence":.5,"summary":f"A simplified inside view of a {name}.","safety_note":"Do not open electrical devices at home. Ask an adult or a trained professional.","parts":[
        {"id":"casing","name":"Outer Casing","shape":"box","size":{"w":1,"h":1,"d":1},"slot":"shell","color":"#cbd5e1","role":"shell","hover_text":"Protects the parts inside.","fun_fact":"Cases are designed to keep dust away from delicate components.","panda_script":"The casing protects the components inside. It is the object’s sturdy outer jacket."},
        {"id":"power","name":"Power Section","shape":"box","size":{"w":.8,"h":.6,"d":.7},"slot":"bottom_left","color":"#60a5fa","role":"power","hover_text":"Supplies power to the device.","fun_fact":"Electronics often use several different voltages.","panda_script":"This section sends the right kind of power around the device. It keeps the whole crew energised."},
        {"id":"core","name":"Main Component","shape":"cylinder","size":{"w":.7,"h":.7,"d":.7},"slot":"center","color":"#fb7185","role":"core","hover_text":"Does the object’s main job.","fun_fact":"Most devices have one part that coordinates the others.","panda_script":"This is the core part doing the main work. It is the team captain inside this object."},
        {"id":"controls","name":"Controls","shape":"box","size":{"w":.7,"h":.4,"d":.5},"slot":"top","color":"#a78bfa","role":"control","hover_text":"Receives commands from the user.","fun_fact":"Controls turn your actions into signals the device can understand.","panda_script":"The controls translate your choices into signals. Pressing a button starts a tiny message passing party."}
    ],"connections":[{"from_id":"power","to_id":"core","label":"powers"},{"from_id":"controls","to_id":"core","label":"commands"}],"flow":["power","controls","core"]})


def laptop_blueprint() -> Blueprint:
    return Blueprint.model_validate({"schema_version":1,"object_name":"Laptop","slug":"laptop","category":"electronics","template":"enclosure","confidence":.78,"summary":"A simplified view of the key parts inside a laptop.","safety_note":"Laptop batteries and chargers should not be opened, punctured, or repaired without a trained adult or technician.","parts":[
        {"id":"casing","name":"Chassis","shape":"box","size":{"w":1,"h":1,"d":1},"slot":"shell","color":"#94a3b8","role":"shell","hover_text":"The strong outer frame holds the laptop together.","fun_fact":"Laptop frames must balance strength with light weight.","panda_script":"This chassis is the laptop’s protective backpack. It keeps the inside team safely in place."},
        {"id":"battery","name":"Battery","shape":"box","size":{"w":.85,"h":.25,"d":.55},"slot":"bottom_left","color":"#60a5fa","role":"power","hover_text":"Stores energy so the laptop can work away from a socket.","fun_fact":"Rechargeable batteries move charged particles back and forth many times.","panda_script":"The battery stores energy for travelling work. It gives every part a portable power snack."},
        {"id":"motherboard","name":"Motherboard","shape":"box","size":{"w":.9,"h":.2,"d":.65},"slot":"center","color":"#a78bfa","role":"core","hover_text":"The main circuit board lets components communicate.","fun_fact":"Tiny copper paths on a motherboard carry electrical signals.","panda_script":"The motherboard is a busy road map for signals. It helps all the laptop parts talk to one another."},
        {"id":"processor","name":"Processor","shape":"box","size":{"w":.4,"h":.22,"d":.4},"slot":"top","color":"#fb7185","role":"core","hover_text":"Performs instructions for apps and tasks.","fun_fact":"A processor can perform billions of tiny steps each second.","panda_script":"The processor follows instructions at super speed. It is the laptop’s quick-thinking problem solver."},
        {"id":"fan","name":"Cooling Fan","shape":"cylinder","size":{"w":.45,"h":.22,"d":.45},"slot":"right","color":"#34d399","role":"cooling","hover_text":"Moves air to help stop components getting too hot.","fun_fact":"Fans move heat away so electronics can work comfortably.","panda_script":"The cooling fan moves warm air away from the processor. It helps the computer stay calm during hard work."}
    ],"connections":[{"from_id":"battery","to_id":"motherboard","label":"powers"},{"from_id":"motherboard","to_id":"processor","label":"signals"},{"from_id":"fan","to_id":"processor","label":"cools"}],"flow":["battery","motherboard","processor"]})


class Pipeline:
    def __init__(self, cache: BlueprintCache, gemini_api_key: str | None = None, gemma_model: str = "gemma-4-26b-a4b-it", gemma_attempt_timeout_seconds: int = 45) -> None:
        self.cache = cache
        self.gemma = GemmaProvider(gemini_api_key, gemma_model, gemma_attempt_timeout_seconds) if gemini_api_key else None

    def demo(self, slug: str) -> Blueprint | None:
        return {"microwave_oven": microwave(), "television": television()}.get(slug)

    def analyze_offline(self, object_name: str | None) -> Blueprint:
        name = object_name or "everyday object"
        known = self.demo(slugify(name))
        return known or fallback_blueprint(name)

    def explain_part(self, object_name: str, part_name: str, role: str, description: str, fact: str) -> str:
        if not self.gemma:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        print(f"[panda] explaining {part_name!r} in {object_name!r}", flush=True)
        return self.gemma.explain_part(object_name, part_name, role, description, fact)

    def analyze_image(self, raw: bytes, mime_type: str, object_name_override: str | None = None) -> Blueprint:
        if not self.gemma:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        print(f"[pipeline] 4/7 preparing a compact image for Gemma | original bytes={len(raw)}", flush=True)
        compact_image = shrink_image(raw)
        print(f"[pipeline] image prepared | JPEG bytes={len(compact_image)}", flush=True)
        print("[pipeline] 5/7 sending a fast object-identification request to Gemini/Gemma...", flush=True)
        detected = self.gemma.identify(compact_image, "image/jpeg", object_name_override)
        print(f"[pipeline] object identified as {detected!r}; building a validated local blueprint", flush=True)
        if "laptop" in detected or "notebook" in detected:
            return laptop_blueprint()
        return self.analyze_offline(object_name_override or detected)
