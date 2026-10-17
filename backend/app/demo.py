from .schemas import Blueprint


def microwave() -> Blueprint:
    return Blueprint.model_validate({
        "schema_version": 1, "object_name": "Microwave Oven", "slug": "microwave_oven", "category": "appliance", "template": "enclosure", "confidence": .95,
        "summary": "Heats food by using microwaves to energise water molecules.",
        "safety_note": "Never open the casing. It can hold dangerous electricity even when unplugged.",
        "parts": [
            {"id":"casing","name":"Metal Casing","shape":"box","size":{"w":1,"h":1,"d":1},"slot":"shell","color":"#cbd5e1","role":"shell","hover_text":"A shield that keeps the microwaves safely inside.","fun_fact":"The tiny door holes are too small for microwaves to escape.","panda_script":"This casing keeps the microwave energy safely trapped inside. It is basically the machine's metal force field, no cap."},
            {"id":"magnetron","name":"Magnetron","shape":"cylinder","size":{"w":.7,"h":.7,"d":.7},"slot":"top_right","color":"#fb7185","role":"core","hover_text":"Creates the microwaves that warm your food.","fun_fact":"Magnetrons were first developed for radar systems.","panda_script":"The magnetron makes the microwaves that heat your food. It is the snack-time main character."},
            {"id":"transformer","name":"Transformer","shape":"box","size":{"w":.8,"h":.6,"d":.8},"slot":"bottom_right","color":"#60a5fa","role":"power","hover_text":"Raises electrical voltage for the magnetron.","fun_fact":"It can increase voltage to thousands of volts.","panda_script":"The transformer gives the magnetron the high voltage it needs. Very powerful, so this part stays safely inside."},
            {"id":"waveguide","name":"Waveguide","shape":"box","size":{"w":.9,"h":.3,"d":.5},"slot":"top","color":"#a78bfa","role":"connector","hover_text":"Guides microwaves toward the food chamber.","fun_fact":"Its shape is tuned to guide a specific microwave wavelength.","panda_script":"The waveguide is a metal tunnel for microwave energy. It sends those invisible waves right where the food is waiting."},
            {"id":"turntable","name":"Turntable","shape":"cylinder","size":{"w":.9,"h":.2,"d":.9},"slot":"bottom","color":"#34d399","role":"moving","hover_text":"Turns food so it heats more evenly.","fun_fact":"Spinning helps avoid icy centers and overheated edges.","panda_script":"The turntable rotates your meal for more even heating. Goodbye frozen middle, hello warm snack vibes."}
        ],
        "connections":[{"from_id":"transformer","to_id":"magnetron","label":"high voltage"},{"from_id":"magnetron","to_id":"waveguide","label":"microwaves"},{"from_id":"waveguide","to_id":"turntable","label":"heats food"}], "flow":["transformer","magnetron","waveguide","turntable"]
    })


def television() -> Blueprint:
    return Blueprint.model_validate({
        "schema_version":1,"object_name":"Television","slug":"television","category":"electronics","template":"stack","confidence":.94,"summary":"Turns electronic signals into moving pictures and sound.","safety_note":"Do not open a TV casing. Internal components can store electrical charge.",
        "parts":[
            {"id":"screen","name":"Display Panel","shape":"box","size":{"w":.95,"h":.8,"d":.3},"slot":"layer_4","color":"#67e8f9","role":"output","hover_text":"Creates the picture you see.","fun_fact":"Each pixel mixes tiny red, green and blue lights.","panda_script":"The display panel lights up millions of tiny pixels to make pictures. Your favorite shows are basically a giant light puzzle."},
            {"id":"backlight","name":"Backlight","shape":"box","size":{"w":.9,"h":.5,"d":.3},"slot":"layer_3","color":"#fde047","role":"output","hover_text":"Shines light through the display panel.","fun_fact":"Modern LED backlights use far less power than old tube lights.","panda_script":"The backlight shines through the display so images can glow. It is like a tiny sun hiding behind the screen."},
            {"id":"main_board","name":"Main Board","shape":"box","size":{"w":.85,"h":.7,"d":.5},"slot":"layer_2","color":"#a78bfa","role":"core","hover_text":"Processes video, sound and button commands.","fun_fact":"It is a small computer made specifically for the TV.","panda_script":"The main board processes every picture and button press. It is the TV's tiny brain, keeping the episode rolling."},
            {"id":"speakers","name":"Speakers","shape":"cylinder","size":{"w":.65,"h":.5,"d":.65},"slot":"layer_1","color":"#fb7185","role":"output","hover_text":"Turns electrical signals into sound waves.","fun_fact":"A speaker cone vibrates back and forth thousands of times a second.","panda_script":"These speakers wiggle the air to make sound you can hear. Tiny vibrations, huge movie-night energy."},
            {"id":"power_board","name":"Power Board","shape":"box","size":{"w":.8,"h":.6,"d":.5},"slot":"layer_0","color":"#60a5fa","role":"power","hover_text":"Converts wall power into safe voltages for the TV.","fun_fact":"Different parts of a TV need different voltages.","panda_script":"The power board turns wall electricity into the right kind of power for each TV part. It is the calm manager behind the scenes."}
        ],"connections":[{"from_id":"power_board","to_id":"main_board","label":"powers"},{"from_id":"main_board","to_id":"screen","label":"video signal"},{"from_id":"main_board","to_id":"speakers","label":"audio signal"}],"flow":["power_board","main_board","backlight","screen","speakers"]
    })


DEMOS = {"microwave_oven": microwave, "television": television}
