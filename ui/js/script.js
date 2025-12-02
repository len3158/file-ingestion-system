function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function getStatusClass(status) {
    const statusLower = status.toLowerCase();

    if (statusLower.includes('success') ||
        statusLower.includes('completed') ||
        statusLower.includes('processed') ||
        statusLower === 'done' ||
        statusLower === 'ok') {
        return 'status-success';
    }

    if (statusLower.includes('error') ||
        statusLower.includes('failed') ||
        statusLower.includes('failure') ||
        statusLower.includes('rejected')) {
        return 'status-error';
    }

    return 'status-pending';
}

async function fetchMetadata() {
    const loading = document.getElementById('loading');
    const table = document.getElementById('metadataTable');
    const emptyState = document.getElementById('emptyState');
    const tbody = document.querySelector('#metadataTable tbody');

    loading.style.display = 'block';
    table.style.display = 'none';
    emptyState.style.display = 'none';

    try {
        const response = await fetch('http://localhost:8080/api/files');
        const data = await response.json();

        tbody.innerHTML = '';

        if (data.length === 0) {
            loading.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }

        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                        <td><strong>${item.filename}</strong></td>
                        <td>${formatBytes(item.size)}</td>
                        <td><span class="hash" title="${item.sha256}">${item.sha256}</span></td>
                        <td><span class="status-badge ${getStatusClass(item.status)}">${item.status}</span></td>
                        <td>${item.reason || '-'}</td>
                        <td>${item.path}</td>
                        <td><button class="retry-btn" onclick="retryFile('${item.filename}')">Retry</button></td>
                    `;
            tbody.appendChild(row);
        });

        loading.style.display = 'none';
        table.style.display = 'table';
    } catch (error) {
        loading.style.display = 'none';
        emptyState.style.display = 'block';
        console.error('Error fetching metadata:', error);
    }
}

async function retryFile(filename) {
    try {
        await fetch(`http://localhost:8080/api/retry/${filename}`, { method: 'POST' });
        await fetchMetadata();
    } catch (error) {
        console.error('Error retrying file:', error);
        alert('Failed to retry file');
    }
}

fetchMetadata().then(r => {});
