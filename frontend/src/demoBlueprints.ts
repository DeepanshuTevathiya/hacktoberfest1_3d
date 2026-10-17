import type { Blueprint } from './types/blueprint';

// These demos are intentionally local: students can explore the app before adding API keys.
const part = (id: string, name: string, slot: string, color: string, role: string, shape: 'box' | 'cylinder', hover: string, fact: string) => ({
  id, name, slot, color, role, shape, size: { w: .72, h: .62, d: .72 }, hover_text: hover, fun_fact: fact,
  panda_script: `${name} has an important job inside this machine. It helps everything work smoothly, with excellent tiny-tech vibes.`,
});

export const localDemos: Record<string, Blueprint> = {
  microwave_oven: {
    schema_version: 1, object_name: 'Microwave Oven', slug: 'microwave_oven', category: 'appliance', template: 'enclosure', confidence: .95,
    summary: 'Heats food by using microwaves to energise water molecules.', safety_note: 'Never open the casing. It can hold dangerous electricity even when unplugged.',
    parts: [
      { ...part('casing', 'Metal Casing', 'shell', '#cbd5e1', 'shell', 'box', 'Keeps microwave energy safely inside.', 'Door mesh holes are too small for microwaves to escape.'), size: { w: 1, h: 1, d: 1 } },
      part('magnetron', 'Magnetron', 'top_right', '#fb7185', 'core', 'cylinder', 'Creates the microwaves that warm food.', 'Magnetrons were first developed for radar.'),
      part('transformer', 'Transformer', 'bottom_right', '#60a5fa', 'power', 'box', 'Raises voltage for the magnetron.', 'It can increase voltage to thousands of volts.'),
      part('waveguide', 'Waveguide', 'top', '#a78bfa', 'connector', 'box', 'Guides microwaves toward the food.', 'Its shape guides a specific wavelength.'),
      part('turntable', 'Turntable', 'bottom', '#34d399', 'moving', 'cylinder', 'Rotates food for even heating.', 'Turning helps prevent cold spots.'),
    ],
    connections: [{ from_id: 'transformer', to_id: 'magnetron', label: 'high voltage' }, { from_id: 'magnetron', to_id: 'waveguide', label: 'microwaves' }], flow: ['transformer', 'magnetron', 'waveguide', 'turntable'],
  },
  television: {
    schema_version: 1, object_name: 'Television', slug: 'television', category: 'electronics', template: 'stack', confidence: .94,
    summary: 'Turns electronic signals into moving pictures and sound.', safety_note: 'Do not open a TV casing. Internal components can store electrical charge.',
    parts: [
      part('power_board', 'Power Board', 'layer_0', '#60a5fa', 'power', 'box', 'Converts wall power for the TV.', 'Different TV parts need different voltages.'),
      part('speakers', 'Speakers', 'layer_1', '#fb7185', 'output', 'cylinder', 'Turn signals into sound waves.', 'A speaker cone vibrates thousands of times a second.'),
      part('main_board', 'Main Board', 'layer_2', '#a78bfa', 'core', 'box', 'Processes video and button commands.', 'It is a small computer just for the TV.'),
      part('backlight', 'Backlight', 'layer_3', '#fde047', 'output', 'box', 'Shines light through the display.', 'LED backlights use much less power than old tube lights.'),
      part('screen', 'Display Panel', 'layer_4', '#67e8f9', 'output', 'box', 'Creates the picture you see.', 'Pixels mix red, green and blue light.'),
    ],
    connections: [{ from_id: 'power_board', to_id: 'main_board', label: 'powers' }, { from_id: 'main_board', to_id: 'screen', label: 'video signal' }], flow: ['power_board', 'main_board', 'backlight', 'screen', 'speakers'],
  },
};
