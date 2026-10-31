/* Render the original licensed CSS, rather than redrawing its animations. */
const fs = require('fs');
const path = require('path');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '..');
const source = path.join(root, 'assets/warder/downloads/ui/spinners/sources/spinkit');
const output = path.join(root, 'assets/warder/downloads/ui/spinners/preview-library/spinkit');
const css = fs.readFileSync(path.join(source, 'spinkit.css'), 'utf8');
const blocks = [...css.matchAll(/\/\*\s*([A-Za-z ]+?)\s*\n([\s\S]*?)\*\//g)]
  .filter(match => match[2].includes('<div')).map(match => ({name:match[1].trim(),html:match[2].trim()}));
const titles = {Plane:'Otáčajúca sa doštička',Chase:'Krúžiace body',Bounce:'Pulzujúce kruhy',
  Wave:'Vlna',Pulse:'Pulz',Flow:'Tri bodky',Swing:'Obiehajúce kruhy',Circle:'Kruh bodiek',
  'Circle Fade':'Postupne svietiaci kruh',Grid:'Mriežka',Fold:'Skladaná kocka',Wander:'Putujúce kocky'};
if (blocks.length !== 12 || blocks.some(item => !titles[item.name])) throw new Error('Unexpected upstream spinner list');
const gcd = (a,b) => b ? gcd(b,a%b) : a;
const lcm = values => values.reduce((a,b) => a*b/gcd(a,b),1);

(async () => {
  const browser = await chromium.launch({headless:true,executablePath:process.env.CHROME_BIN || undefined,
    args:['--no-sandbox','--disable-gpu','--force-color-profile=srgb']});
  try {
    const context = await browser.newContext({viewport:{width:104,height:104},deviceScaleFactor:4,
      colorScheme:'dark',reducedMotion:'no-preference'});
    const page = await context.newPage();
    await page.route('**/*', route => route.abort());
    const rows = [];
    for (let index=0;index<blocks.length;index++) {
      const item=blocks[index];
      const slug=item.name.toLowerCase().replace(/ /g,'-');
      const folder=path.join(output,String(index+1).padStart(2,'0')+'-'+slug);
      fs.mkdirSync(path.join(folder,'rendered'),{recursive:true});
      await page.setContent(`<!doctype html><html><head><style>${css}\n
        :root{--sk-size:64px;--sk-color:#3CCFFF}
        html,body{margin:0;width:104px;height:104px;background:transparent;overflow:hidden}
        body{display:grid;place-items:center}
        /* Synchronize existing two-second subanimations for a seamless native loop. */
        .sk-chase,.sk-swing{animation-duration:2s}
      </style></head><body>${item.html}</body></html>`);
      const timing=await page.evaluate(() => document.getAnimations().map(animation => {
        animation.pause(); animation.currentTime=0;
        const value=animation.effect.getTiming();
        return {duration:Math.round(Number(value.duration)),direction:value.direction};
      }));
      if (!timing.length || timing.some(item=>!(item.duration>0))) throw new Error('Missing CSS animation');
      const period=lcm(timing.map(item=>item.duration*(item.direction.includes('alternate')?2:1)));
      const count=period/100;
      if (!Number.isInteger(count)||count<2||count>64) throw new Error('Unsupported native cycle '+period);
      for (let frame=0;frame<count;frame++) {
        await page.evaluate(time => document.getAnimations().forEach(animation => {animation.currentTime=time;}),frame*100);
        await page.screenshot({path:path.join(folder,'rendered','wait'+(frame+1)+'.png'),omitBackground:true});
      }
      const row={id:'spinkit-'+slug,folder:path.basename(folder),name:item.name,title:titles[item.name],
        author:'Tobias Ahlin',license:'MIT',source_commit:'742a71277c49b69053b5beb9fad80d720840a2ab',
        source_url:'https://github.com/tobiasahlin/SpinKit',frame_count:count,interval_ms:100,size:[104,104],
        color:'#3CCFFF',inner_css_size:64,css_render_scale:4,native_cycle_ms:period,
        timing_adaptation:['Chase','Swing'].includes(item.name)?'Container synchronized to the existing two-second child animation; original geometry and keyframes preserved.':'Original cycle preserved.',
        state:'preview-only-not-installed'};
      fs.writeFileSync(path.join(folder,'metadata.json'),JSON.stringify(row,null,2)+'\n');
      rows.push(row); console.log('Rendered '+row.folder+': '+count+' frames');
    }
    fs.writeFileSync(path.join(output,'catalog.json'),JSON.stringify({schema:1,author:'Tobias Ahlin',license:'MIT',entries:rows},null,2)+'\n');
    console.log('CSS browser rendering complete');
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
