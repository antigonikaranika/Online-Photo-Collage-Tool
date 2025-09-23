const imageInput = document.getElementById('image-input');
const imageList = document.getElementById('image-list');
const createBtn = document.getElementById('create-btn');
const previewArea = document.getElementById('preview-area');
const downloadLink = document.getElementById('download-link');

let files = [];

imageInput.addEventListener('change', (e) => {
  for (const file of e.target.files) {
    files.push(file);
  }
  renderFileList();
});

function renderFileList() {
  imageList.innerHTML = '';
  files.forEach((file, index) => {
    const li = document.createElement('li');
    li.className = 'image-item';
    li.innerHTML = `
      <span>${file.name}</span>
      <button onclick="removeFile(${index})">✖</button>
    `;
    imageList.appendChild(li);
  });
}

function removeFile(index) {
  files.splice(index, 1);
  renderFileList();
}

createBtn.addEventListener('click', async () => {
  if (files.length === 0) {
    alert("Please upload at least one image.");
    return;
  }

  const formData = new FormData();
  files.forEach(file => formData.append('images', file));
  formData.append('collage_type', document.querySelector('input[name="type"]:checked').value);
  formData.append('border_size', document.getElementById('border-size').value);
  formData.append('border_color', document.getElementById('border-color').value);

  previewArea.innerHTML = '<p>Creating collage...</p>';
  downloadLink.style.display = 'none';

  const response = await fetch('/create-task', {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  const taskId = data.task_id;

  checkStatus(taskId);
});

async function checkStatus(taskId) {
  const interval = setInterval(async () => {
    const res = await fetch(`/task-status/${taskId}`);
    const data = await res.json();

    if (data.state === 'SUCCESS') {
      clearInterval(interval);
      const collageId = data.result.collage_id;
      const collageUrl = `/get-collage/${collageId}`;
      previewArea.innerHTML = `<img src="${collageUrl}" alt="Collage">`;
      downloadLink.href = collageUrl;
      downloadLink.style.display = 'inline-block';
    } else if (data.state === 'FAILURE') {
      clearInterval(interval);
      previewArea.innerHTML = `<p style="color:red;">Failed: ${data.error}</p>`;
    }
  }, 2000);
}