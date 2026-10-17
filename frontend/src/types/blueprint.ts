export type Template = 'enclosure' | 'stack' | 'radial' | 'chain' | 'mechanism';
export type Shape = 'box' | 'cylinder' | 'sphere' | 'cone' | 'torus' | 'capsule';
export interface Part { id:string; name:string; shape:Shape; size:{w:number;h:number;d:number}; slot:string; color:string; role:string; hover_text:string; fun_fact:string; panda_script:string }
export interface Blueprint { schema_version:1; object_name:string; slug:string; category:string; template:Template; confidence:number; summary:string; safety_note:string|null; parts:Part[]; connections:{from_id:string;to_id:string;label:string}[]; flow:string[] }
