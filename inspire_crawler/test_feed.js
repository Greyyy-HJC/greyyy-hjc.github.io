// Exercise the browser refresh and fallback without a browser dependency.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const template = fs.readFileSync(path.join(root, '_includes/fetch_inspire_publications.html'), 'utf8');
const source = template.replace(/<\/?script>/g, '')
  .replaceAll('{{ site.repository }}', 'Greyyy-HJC/greyyy-hjc.github.io')
  .replaceAll('{{ site.data.inspire_config.feed_branch }}', 'inspire-stats')
  .replaceAll('{{ site.data.inspire_config.author_id }}', '1935435');

async function run(data, status = true) {
  const target = {innerHTML: 'snapshot'};
  const summary = {textContent: '', appendChild() {}};
  const document = {
    getElementById(id) { return id === 'inspire-publication-list' ? target : summary; },
    createElement() { return {}; },
  };
  let fetchedUrl;
  vm.runInNewContext(source, {
    document, AbortController, setTimeout, clearTimeout,
    fetch: async url => { fetchedUrl = url; return {ok: status, json: async () => data}; },
  });
  await new Promise(resolve => setImmediate(resolve));
  return {target, summary, fetchedUrl};
}

(async () => {
  const data = {schema_version: 1, author_id: '1935435', publications: [{id: '1'}], html: '<ul><li>new</li></ul>', total_citations: 2};
  const success = await run(data);
  assert.equal(success.target.innerHTML, data.html);
  assert.match(success.summary.textContent, /2 INSPIRE citations/);
  assert.match(success.fetchedUrl, /Greyyy-HJC\/greyyy-hjc.github.io\/inspire-stats\/inspire_data.json$/);
  for (const invalid of [{...data, author_id: '999'}, {...data, publications: []}, {...data, schema_version: 2}]) {
    assert.equal((await run(invalid)).target.innerHTML, 'snapshot');
  }
  assert.equal((await run(data, false)).target.innerHTML, 'snapshot');
  console.log('Browser refresh and offline/invalid-feed fallback checks passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
