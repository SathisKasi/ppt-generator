const input = document.querySelector('#fileInput');
const dropzone = document.querySelector('#dropzone');
const choose = document.querySelector('#chooseButton');
const resetButton = document.querySelector('#resetButton');
const generate = document.querySelector('#generateButton');
const fileName = document.querySelector('#fileName');
const error = document.querySelector('#error');
const label = document.querySelector('#statusLabel');
const templateSelect = document.querySelector('#templateSelect');
const slideCountSelect = document.querySelector('#slideCountSelect');
const topicNameInput = document.querySelector('#topicNameInput');
const presentedByInput = document.querySelector('#presentedByInput');
const download = document.querySelector('#downloadButton');
let selected;
let fileId;

function resetPage() {
  selected = undefined;
  fileId = undefined;
  input.value = '';
  fileName.textContent = 'No file selected';
  generate.disabled = true;
  error.textContent = '';
  label.textContent = 'Waiting';
  disableDownload();
  document.querySelectorAll('#steps li').forEach(step => step.classList.remove('complete'));
}

function disableDownload() {
  download.removeAttribute('href');
  download.classList.add('disabled');
  download.setAttribute('aria-disabled', 'true');
}

function enableDownload(id) {
  download.href = `/api/download/${id}`;
  download.classList.remove('disabled');
  download.setAttribute('aria-disabled', 'false');
}

download.addEventListener('click', event => {
  if (download.classList.contains('disabled')) {
    event.preventDefault();
    return;
  }
  window.setTimeout(resetPage, 250);
});

fetch('/api/templates').then(response => response.json()).then(payload => {
  templateSelect.replaceChildren(...payload.templates.map(template => {
    const option = document.createElement('option');
    option.value = template.id;
    option.textContent = template.name;
    option.title = template.description;
    return option;
  }));
  if (templateSelect.options.length > 0) {
    templateSelect.selectedIndex = 0;
  }
}).catch(() => { templateSelect.innerHTML = '<option value="ups-healthcare">UPS Healthcare Executive</option>'; });

choose.addEventListener('click', () => input.click());
if (resetButton) {
  resetButton.addEventListener('click', resetPage);
}
input.addEventListener('change', () => selectFile(input.files[0]));
['dragenter', 'dragover'].forEach(name => dropzone.addEventListener(name, event => { event.preventDefault(); dropzone.classList.add('dragging'); }));
['dragleave', 'drop'].forEach(name => dropzone.addEventListener(name, event => { event.preventDefault(); dropzone.classList.remove('dragging'); }));
dropzone.addEventListener('drop', event => selectFile(event.dataTransfer.files[0]));

const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.pptx', '.xlsx', '.csv', '.txt', '.md', '.markdown'];

function selectFile(file) {
  if (!file) return;
  const fileNameLower = (file.name || '').toLowerCase();
  const isAllowed = ALLOWED_EXTENSIONS.some(ext => fileNameLower.endsWith(ext));
  if (!isAllowed) {
    selected = undefined;
    fileId = undefined;
    input.value = '';
    fileName.textContent = 'No file selected';
    generate.disabled = true;
    error.textContent = 'Invalid file format. Only PDF, DOCX, PPTX, XLSX, CSV, TXT, and Markdown files are supported.';
    label.textContent = 'Invalid file';
    disableDownload();
    return;
  }
  selected = file;
  fileId = undefined;
  fileName.textContent = `${file.name} - ${(file.size / 1024).toFixed(1)} KB`;
  generate.disabled = false;
  error.textContent = '';
  label.textContent = 'Ready';
  disableDownload();
}

generate.addEventListener('click', async () => {
  const topicName = topicNameInput.value.trim();
  const presentedBy = presentedByInput.value.trim();
  if (!topicName || !presentedBy) {
    error.textContent = 'Presentation Topic Name and Presented By are required.';
    label.textContent = 'Needs attention';
    return;
  }
  generate.disabled = true;
  label.textContent = 'Processing';
  error.textContent = '';
  disableDownload();
  try {
    const body = new FormData();
    body.append('file', selected);
    const upload = await fetch('/api/upload', { method: 'POST', body });
    const uploaded = await upload.json();
    if (!upload.ok) throw new Error(uploaded.detail || 'Upload failed');
    fileId = uploaded.file_id;
    mark('uploaded');
    const templateId = templateSelect.value || 'ups-healthcare';
    const slideCount = slideCountSelect.value || '8';
    const response = await fetch(`/api/generate-presentation?file_id=${encodeURIComponent(fileId)}&template_id=${encodeURIComponent(templateId)}&slide_count=${encodeURIComponent(slideCount)}&topic_name=${encodeURIComponent(topicName)}&presented_by=${encodeURIComponent(presentedBy)}`, { method: 'POST' });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Generation failed');
    ['extracted', 'analyzed', 'planned', 'generated'].forEach(mark);
    label.textContent = 'Complete';
    enableDownload(fileId);
  } catch (reason) {
    label.textContent = 'Needs attention';
    error.textContent = reason.message;
    generate.disabled = false;
  }
});

function mark(step) { document.querySelector(`[data-step="${step}"]`).classList.add('complete'); }
