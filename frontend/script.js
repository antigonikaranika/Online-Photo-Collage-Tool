document.getElementById('collageForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = document.getElementById('collageForm');
    const formData = new FormData(form);

    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    result.innerHTML = '';
    loading.style.display = 'block';

    try {
        const response = await fetch('/create-task', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error creating task.');
        }

        const data = await response.json();
        const taskId = data.task_id;

        const checkStatus = setInterval(async () => {
            const statusResponse = await fetch(`/task-status/${taskId}`);
            const statusData = await statusResponse.json();

            if (statusData.state === 'SUCCESS') {
                clearInterval(checkStatus);
                loading.style.display = 'none';

                const collageId = statusData.result.collage_id;
                result.innerHTML = `
                    <h3>Collage Created Successfully!</h3>
                    <img src="/get-collage/${collageId}" alt="Your Collage">
                    <br><a href="/get-collage/${collageId}" download>Download Collage</a>
                `;
            } else if (statusData.state === 'FAILURE') {
                clearInterval(checkStatus);
                loading.style.display = 'none';
                result.innerHTML = `<p style="color:red;">Error: ${statusData.error}</p>`;
            }
        }, 3000);
    } catch (error) {
        loading.style.display = 'none';
        result.innerHTML = `<p style="color:red;">${error.message}</p>`;
    }
});
