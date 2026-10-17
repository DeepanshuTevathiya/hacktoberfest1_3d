import { describe, expect, it } from 'vitest';
import { layoutBlueprint } from './index';
import type { Blueprint, Template } from '../types/blueprint';

const make = (template: Template, slots: string[]): Blueprint => ({
  schema_version: 1, object_name: 'Test', slug: 'test', category: 'other', template, confidence: 1, summary: 'Test', safety_note: null,
  parts: slots.map((slot, i) => ({ id: `part_${i}`, name: 'Part', shape: 'box', size: { w: .5, h: .5, d: .5 }, slot, color: '#ffffff', role: 'core', hover_text: 'Does a thing', fun_fact: 'A true fact', panda_script: 'This part does its job very well indeed.' })),
  connections: [], flow: slots.slice(0, 3).map((_, i) => `part_${i}`),
});

describe('layout engine', () => {
  it('maps every template to cells', () => {
    const examples: [Template, string[]][] = [
      ['enclosure', ['shell', 'center', 'top']], ['stack', ['layer_0', 'layer_1', 'layer_2']], ['radial', ['center', 'ring_0', 'ring_1']], ['chain', ['step_0', 'step_1', 'step_2']], ['mechanism', ['r0c0', 'r1c1', 'r2c2']],
    ];
    for (const [template, slots] of examples) expect(Object.keys(layoutBlueprint(make(template, slots)))).toHaveLength(3);
  });
  it('keeps parts inside the 4 unit world', () => {
    for (const item of Object.values(layoutBlueprint(make('mechanism', ['r0c0', 'r1c1', 'r2c2'])))) item.position.forEach((x, i) => expect(Math.abs(x) + item.dimensions[i] / 2).toBeLessThanOrEqual(2));
  });
  it('rejects invalid slots', () => expect(() => layoutBlueprint(make('chain', ['wrong', 'step_1', 'step_2']))).toThrow('Invalid slot'));
});
