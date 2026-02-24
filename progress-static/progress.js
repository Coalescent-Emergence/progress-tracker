// progress.js
// Loads and displays MVP progress from static progress.json

async function fetchProjectV2Issues() {
  try {
    const res = await fetch('progress.json');
    if (!res.ok) throw new Error('progress.json not found');
    return await res.json();
  } catch (e) {
    document.getElementById('progress-summary').textContent = 'Progress data not available.';
    return null;
  }
}

function summarizeProgress(issues) {
  const total = issues.length;
  const closed = issues.filter(i => i.content && i.content.state === 'CLOSED').length;
  return { total, closed, percent: total ? Math.round((closed / total) * 100) : 0 };
}

function renderProgress(issues) {
  const summary = summarizeProgress(issues);
  document.getElementById('progress-summary').innerHTML =
    `<strong>${summary.closed}</strong> of <strong>${summary.total}</strong> issues closed (<strong>${summary.percent}%</strong> complete)`;

  const list = document.getElementById('issue-list');
  list.innerHTML = '';
  issues.forEach(i => {
    if (!i.content) return;
    const li = document.createElement('li');
    li.className = 'issue';
    li.innerHTML = `
      <a href="${i.content.url}" target="_blank">#${i.content.number}: ${i.content.title}</a>
      <span class="status-${i.content.state.toLowerCase()}" style="float:right;">${i.content.state}</span>
      <div>Labels: ${(i.content.labels.nodes.map(l => l.name).join(', ') || 'None')}</div>
    `;
    list.appendChild(li);
  });
}

async function main() {
  const issues = await fetchProjectV2Issues();
  if (issues) renderProgress(issues);
}

main();
