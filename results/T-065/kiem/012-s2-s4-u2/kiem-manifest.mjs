import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const digest=b=>({sha256:crypto.createHash('sha256').update(b).digest('hex'),bytes:b.length});
export async function kiemManifest(taskRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..')) {
  const manifest=JSON.parse(await fs.readFile(path.join(taskRoot,'manifest.json'),'utf8'));
  const queue=Object.entries(manifest.files);
  const errors=[]; let next=0;
  await Promise.all(Array.from({length:16},async()=>{
    while(next<queue.length){
      const [rel,pin]=queue[next++];
      try {
        const actual=digest(await fs.readFile(path.join(taskRoot,rel)));
        if(actual.sha256!==pin.sha256||actual.bytes!==pin.bytes)errors.push({file:rel,expected:pin,actual});
      } catch(error) { errors.push({file:rel,error:error.code??String(error)}); }
    }
  }));
  const repoRoot=path.resolve(taskRoot,'../..');
  const external=[manifest.task_log,...(manifest.task_reviews??[manifest.task_review])].filter(Boolean);
  for(const pin of external){
    try {
      const actual=digest(await fs.readFile(path.join(repoRoot,pin.file)));
      if(actual.sha256!==pin.sha256||actual.bytes!==pin.bytes)errors.push({file:pin.file,expected:pin,actual});
    } catch(error) { errors.push({file:pin.file,error:error.code??String(error)}); }
  }
  return {utc:new Date().toISOString(),files_checked:queue.length,external_checked:external.length,passed:errors.length===0,errors};
}
