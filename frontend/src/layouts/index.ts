import type { Blueprint, Part, Template } from '../types/blueprint';
export type Vec3=[number,number,number]; export interface LayoutItem {position:Vec3; dimensions:Vec3; explode:Vec3}
const pad=(n:number)=>n*.9;
const cell=(c:Vec3,d:Vec3)=>({center:c,dims:d});
function cells(template:Template, count:number):Record<string,{center:Vec3;dims:Vec3}>{
 const out:Record<string,{center:Vec3;dims:Vec3}>={};
 if(template==='enclosure'){out.shell=cell([0,0,0],[4,4,4]); Object.assign(out,{top_left:cell([-1,1,0],[1.6,1.6,2.8]),top_right:cell([1,1,0],[1.6,1.6,2.8]),bottom_left:cell([-1,-1,0],[1.6,1.6,2.8]),bottom_right:cell([1,-1,0],[1.6,1.6,2.8]),top:cell([0,1.45,0],[1.6,.7,2.8]),bottom:cell([0,-1.45,0],[1.6,.7,2.8]),left:cell([-1.45,0,0],[.7,1.6,2.8]),right:cell([1.45,0,0],[.7,1.6,2.8]),center:cell([0,0,0],[1.2,1.2,1.5]),front:cell([0,0,1.15],[1.6,1.6,.5]),back:cell([0,0,-1.15],[1.6,1.6,.5])});}
 if(template==='stack') for(let i=0;i<10;i++) out[`layer_${i}`]=cell([0,-1.8+(i+.5)*.4,0],[3.4,.34,2.8]);
 if(template==='radial'){out.center=cell([0,0,0],[1.1,1.5,1.1]); for(let i=0;i<9;i++){const a=i/9*Math.PI*2;out[`ring_${i}`]=cell([1.35*Math.cos(a),0,1.35*Math.sin(a)],[.7,1.2,.7]);}}
 if(template==='chain') for(let i=0;i<10;i++)out[`step_${i}`]=cell([-1.8+(i+.5)*.36,0,0],[.3,2.8,2.8]);
 if(template==='mechanism') for(let r=0;r<3;r++)for(let c=0;c<3;c++)out[`r${r}c${c}`]=cell([-1.25+c*1.25,1.25-r*1.25,0],[1.1,1.1,.7]);
 return out;
}
export function layoutBlueprint(blueprint:Blueprint):Record<string,LayoutItem>{const result:Record<string,LayoutItem>={};const slots=cells(blueprint.template,blueprint.parts.length);for(const part of blueprint.parts){const c=slots[part.slot];if(!c) throw new Error(`Invalid slot ${part.slot}`);const d:[number,number,number]=[pad(c.dims[0]*part.size.w),pad(c.dims[1]*part.size.h),pad(c.dims[2]*part.size.d)];const len=Math.hypot(...c.center)||1;result[part.id]={position:c.center,dimensions:d,explode:[c.center[0]/len,c.center[1]/len,c.center[2]/len]};}return result;}
