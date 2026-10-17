import { create } from 'zustand'; import type { Blueprint } from '../types/blueprint';
type Status='upload'|'loading'|'viewer'|'error';
interface State {status:Status; blueprint?:Blueprint; selectedPartId?:string; hoveredPartId?:string; explodeValue:number; error?:string; set:(patch:Partial<State>)=>void; reset:()=>void}
export const useStore=create<State>((set)=>({status:'upload',explodeValue:0,set:(patch)=>set(patch),reset:()=>set({status:'upload',blueprint:undefined,selectedPartId:undefined,hoveredPartId:undefined,error:undefined,explodeValue:0})}));
