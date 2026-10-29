import {build} from 'esbuild';
await build({entryPoints:['src/dk-raydium.ts'],bundle:true,format:'esm',platform:'browser',minify:true,target:'es2020',outfile:'../assets/dk-raydium.js',
 define:{'process.env.NODE_ENV':'"production"','global':'globalThis'},
 inject:['shim.js'],legalComments:'none'});
