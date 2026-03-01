const STORAGE_KEY = 'portfolioHubProfile_v1';

function $(id) {
  return document.getElementById(id);
}

function loadProfile() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function saveProfile(profile) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
}

function getProfileFromForm() {
  return {
    fullName: $('fullName').value.trim(),
    headline: $('headline').value.trim(),
    github: $('github').value.trim(),
    linkedin: $('linkedin').value.trim(),
    leetcode: $('leetcode').value.trim(),
    otherLinks: $('otherLinks')
      .value.split('\n')
      .map((l) => l.trim())
      .filter(Boolean),
    bio: $('bio').value.trim(),
  };
}

function populateForm(profile) {
  if (!profile) return;
  $('fullName').value = profile.fullName || '';
  $('headline').value = profile.headline || '';
  $('github').value = profile.github || '';
  $('linkedin').value = profile.linkedin || '';
  $('leetcode').value = profile.leetcode || '';
  $('otherLinks').value = (profile.otherLinks || []).join('\n');
  $('bio').value = profile.bio || '';
}

function renderPortfolioPreview(profile) {
  const container = $('portfolio-preview');
  container.innerHTML = '';

  const safeProfile = profile || {
    fullName: 'Your name',
    headline: 'Your headline',
    github: '',
    linkedin: '',
    leetcode: '',
    otherLinks: [],
    bio: 'Write a short bio so people instantly understand who you are and what you do.',
  };

  const left = document.createElement('div');
  left.className = 'preview-left';

  const nameEl = document.createElement('div');
  nameEl.className = 'preview-name';
  nameEl.textContent = safeProfile.fullName || 'Your name';

  const headlineEl = document.createElement('div');
  headlineEl.className = 'preview-headline';
  headlineEl.textContent = safeProfile.headline || 'Your headline';

  const bioEl = document.createElement('div');
  bioEl.className = 'preview-bio';
  bioEl.textContent = safeProfile.bio || safeProfile.bio;

  const chipRow = document.createElement('div');
  chipRow.className = 'chip-row';

  if (safeProfile.github) {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.textContent = 'GitHub';
    chipRow.appendChild(chip);
  }
  if (safeProfile.leetcode) {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.textContent = 'LeetCode';
    chipRow.appendChild(chip);
  }
  if (safeProfile.linkedin) {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.textContent = 'LinkedIn';
    chipRow.appendChild(chip);
  }

  left.appendChild(nameEl);
  left.appendChild(headlineEl);
  left.appendChild(bioEl);
  if (chipRow.children.length) {
    left.appendChild(chipRow);
  }

  const right = document.createElement('div');
  right.className = 'link-list';

  function makeLink(label, href, subtle) {
    if (!href) return null;
    const link = document.createElement('a');
    link.className = 'profile-link';
    link.href = href;
    link.target = '_blank';
    link.rel = 'noreferrer';

    const dot = document.createElement('span');
    dot.className = 'link-dot';

    const text = document.createElement('span');
    text.textContent = label;

    const small = document.createElement('small');
    small.textContent = subtle;

    link.appendChild(dot);
    link.appendChild(text);
    link.appendChild(small);
    return link;
  }

  if (safeProfile.github) {
    const url = safeProfile.github.startsWith('http')
      ? safeProfile.github
      : `https://github.com/${safeProfile.github}`;
    right.appendChild(makeLink('GitHub', url, safeProfile.github));
  }
  if (safeProfile.linkedin) {
    right.appendChild(makeLink('LinkedIn', safeProfile.linkedin, 'Profile'));
  }
  if (safeProfile.leetcode) {
    const url = safeProfile.leetcode.startsWith('http')
      ? safeProfile.leetcode
      : `https://leetcode.com/${safeProfile.leetcode}`;
    right.appendChild(makeLink('LeetCode', url, safeProfile.leetcode));
  }

  (safeProfile.otherLinks || []).forEach((raw, index) => {
    if (!raw) return;
    const url = raw.startsWith('http') ? raw : `https://${raw}`;
    right.appendChild(makeLink(`Link ${index + 1}`, url, raw));
  });

  container.appendChild(left);
  container.appendChild(right);
}

async function generateResume() {
  const statusEl = $('ai-status');
  const outputEl = $('resumeOutput');
  const copyBtn = $('copyResume');

  statusEl.textContent = '';
  statusEl.classList.remove('error');

  const apiBaseUrl = $('apiBaseUrl').value.trim() || 'https://api.openai.com';
  const apiKey = $('apiKey').value.trim();
  const modelName = $('modelName').value.trim() || 'gpt-4.1-mini';
  const roleTarget = $('roleTarget').value.trim();
  const extra = $('extraInstructions').value.trim();

  if (!apiKey) {
    statusEl.textContent = 'Please provide an API key.';
    statusEl.classList.add('error');
    return;
  }

  const profile = loadProfile() || getProfileFromForm();

  const systemPrompt =
    'You are an expert resume writer for software engineers. ' +
    'Given data about a developer and links to their profiles, write a concise, ATS-friendly resume. ' +
    'Focus on impact, metrics, and clear bullet points. Use clean Markdown formatting only.';

  const userPrompt = [
    'Use the following profile information and links to write a tailored resume.',
    '',
    `Target role / industry: ${roleTarget || 'Not specified'}`,
    '',
    'Profile data (JSON):',
    '```json',
    JSON.stringify(profile, null, 2),
    '```',
    '',
    extra ? `Extra instructions: ${extra}` : '',
  ].join('\n');

  const body = {
    model: modelName,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ],
  };

  $('generateResume').disabled = true;
  $('generateResume').textContent = 'Generating…';
  copyBtn.disabled = true;
  statusEl.textContent = 'Calling the AI API…';

  try {
    const response = await fetch(`${apiBaseUrl.replace(/\/+$/, '')}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API error (${response.status}): ${errorText.slice(0, 200)}`);
    }

    const data = await response.json();
    const content =
      data.choices?.[0]?.message?.content ||
      'The AI did not return any content. Please check your model and try again.';

    outputEl.value = content;
    copyBtn.disabled = !content;
    statusEl.textContent = 'Resume generated successfully.';
  } catch (err) {
    console.error(err);
    statusEl.textContent = 'Failed to generate resume. Check console for details.';
    statusEl.classList.add('error');
  } finally {
    $('generateResume').disabled = false;
    $('generateResume').textContent = 'Generate resume';
  }
}

function attachEventHandlers() {
  const form = $('profile-form');
  const statusEl = $('profile-status');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const profile = getProfileFromForm();
    saveProfile(profile);
    renderPortfolioPreview(profile);
    statusEl.textContent = 'Profile saved locally.';
    statusEl.classList.remove('error');
  });

  $('resetProfile').addEventListener('click', () => {
    localStorage.removeItem(STORAGE_KEY);
    populateForm({
      fullName: '',
      headline: '',
      github: '',
      linkedin: '',
      leetcode: '',
      otherLinks: [],
      bio: '',
    });
    renderPortfolioPreview(null);
    statusEl.textContent = 'Profile cleared.';
    statusEl.classList.remove('error');
  });

  $('generateResume').addEventListener('click', () => {
    generateResume();
  });

  $('copyResume').addEventListener('click', async () => {
    const output = $('resumeOutput').value;
    if (!output) return;
    try {
      await navigator.clipboard.writeText(output);
      $('ai-status').textContent = 'Copied resume to clipboard.';
      $('ai-status').classList.remove('error');
    } catch {
      $('ai-status').textContent = 'Unable to copy to clipboard.';
      $('ai-status').classList.add('error');
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
  const stored = loadProfile();
  populateForm(stored);
  renderPortfolioPreview(stored);
  attachEventHandlers();
});

