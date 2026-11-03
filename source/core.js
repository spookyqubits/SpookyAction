(function (root, make) {
  const api = make();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.SpookyActionCore = api;
})(typeof globalThis === 'object' ? globalThis : this, function () {
  'use strict';
  const P = Math.cos(Math.PI / 8) ** 2;
  const DEFINITIONS = {
    trio: {name:'Ghost Trio',slug:'ghost-trio',n:3,labels:['X','Y'],cases:[[0,0,0],[0,1,1],[1,0,1],[1,1,0]],quantum:1},
    twins: {name:'Ghost Twins',slug:'ghost-twins',n:2,labels:['0','1'],cases:[[0,0],[0,1],[1,0],[1,1]],quantum:P}
  };
  const bit = x => x === 0 || x === 1;
  function definition(kind) {if(!DEFINITIONS[kind])throw Error('Unknown game');return DEFINITIONS[kind];}
  function checkCase(kind, questions) {
    const d=definition(kind);
    if(!Array.isArray(questions)||!d.cases.some(q=>q.length===questions.length&&q.every((x,i)=>x===questions[i])))throw Error('Invalid question card');
    return d;
  }
  function validPlan(kind, plan) {return Array.isArray(plan)&&plan.length===definition(kind).n&&plan.every(row=>Array.isArray(row)&&row.length===2&&row.every(bit));}
  function target(kind, questions) {checkCase(kind,questions);return kind==='trio'?Number(questions.some(Boolean)):questions[0]&questions[1];}
  function wins(kind, questions, answers) {
    const d=checkCase(kind,questions);
    if(!Array.isArray(answers)||answers.length!==d.n||!answers.every(bit))throw Error('Invalid answers');
    return answers.reduce((a,b)=>a^b,0)===target(kind,questions);
  }
  function answersFor(kind, plan, questions) {checkCase(kind,questions);if(!validPlan(kind,plan))throw Error('Invalid plan');return questions.map((q,i)=>plan[i][q]);}
  function coverage(kind,plan) {return definition(kind).cases.filter(q=>wins(kind,q,answersFor(kind,plan,q))).length;}
  function joint(kind,questions) {
    const d=checkCase(kind,questions),p=d.quantum;
    return Array.from({length:2**d.n},(_,v)=>{
      const answers=Array.from({length:d.n},(_,i)=>(v>>(d.n-i-1))&1);
      return {answers,p:(wins(kind,questions,answers)?p:1-p)/(2**(d.n-1))};
    });
  }
  function random() {
    if(typeof globalThis.crypto?.getRandomValues==='function'){const a=new Uint32Array(1);globalThis.crypto.getRandomValues(a);return a[0]/4294967296;}
    return Math.random();
  }
  function draw(rng) {const u=rng();if(!Number.isFinite(u)||u<0||u>=1)throw Error('Invalid random draw');return u;}
  function sample(kind,questions,rng=random) {
    const u=draw(rng),outcomes=joint(kind,questions);let c=0;
    for(const outcome of outcomes){c+=outcome.p;if(u<c)return outcome.answers.slice();}
    return outcomes.at(-1).answers.slice();
  }
  function deck(kind,rng=random) {
    const out=definition(kind).cases.map(q=>q.slice());
    for(let i=out.length-1;i>0;i--){const j=Math.floor(draw(rng)*(i+1));[out[i],out[j]]=[out[j],out[i]];}
    return out;
  }
  function strategies(kind) {
    const n=definition(kind).n;
    return Array.from({length:2**(2*n)},(_,v)=>{
      const plan=Array.from({length:n},(_,i)=>[(v>>(2*i))&1,(v>>(2*i+1))&1]);
      return {plan,hits:coverage(kind,plan)};
    });
  }
  function emptyStats() {return {n:0,classical:0,quantum:0,cases:Array.from({length:4},()=>({n:0,classical:0,quantum:0}))};}
  function benchmark(kind,plan,n=100,rng=random) {
    const d=definition(kind);if(!validPlan(kind,plan)||!Number.isInteger(n)||n<1||n>10000)throw Error('Invalid batch');
    const s=emptyStats();
    for(let i=0;i<n;i++){
      const index=Math.floor(draw(rng)*4),q=d.cases[index],c=Number(wins(kind,q,answersFor(kind,plan,q))),g=Number(wins(kind,q,sample(kind,q,rng)));
      s.n++;s.classical+=c;s.quantum+=g;const row=s.cases[index];row.n++;row.classical+=c;row.quantum+=g;
    }
    return s;
  }
  function merge(a,b) {return {n:a.n+b.n,classical:a.classical+b.classical,quantum:a.quantum+b.quantum,cases:a.cases.map((r,i)=>({n:r.n+b.cases[i].n,classical:r.classical+b.cases[i].classical,quantum:r.quantum+b.cases[i].quantum}))};}
  return {DEFINITIONS,P,definition,validPlan,target,wins,answersFor,coverage,joint,sample,deck,strategies,emptyStats,benchmark,merge,random};
});
