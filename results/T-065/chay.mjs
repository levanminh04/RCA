// Node có JSON.rawJSON (Node 22+). Không cài package, không chạy lại M1.
import {build} from './xuat-du-lieu.mjs';
import {buildDashboards} from './dung-dashboard.mjs';
import {verify} from './kiem.mjs';
console.log(await build());
console.log(await buildDashboards());
const result=await verify();
console.log({schema:result.schema.length,links:result.links,cases:result.cases.length});
