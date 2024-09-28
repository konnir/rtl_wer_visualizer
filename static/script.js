document.getElementById('voice-file-btn').addEventListener('click', () => {
    document.getElementById('voice-file-input').click();
});

document.getElementById('reference-file-btn').addEventListener('click', () => {
    document.getElementById('reference-file-input').click();
});

document.getElementById('check-btn').addEventListener('click', async () => {
    // Clear the screen
    document.getElementById('output-text').innerHTML = '';

    const voiceFile = document.getElementById('voice-file-input').files[0];
    const referenceFile = document.getElementById('reference-file-input').files[0];
    const useCustomIp = document.getElementById('use-custom-ip').checked;
    const customIp = document.getElementById('custom-ip').value;
    const serverUrl = document.getElementById('server-url').value;

    // Determine whether to use the custom IP or the selected server URL
    const finalUrl = useCustomIp && customIp ? customIp : serverUrl;

    if (!voiceFile || !referenceFile) {
        alert('Please select both voice and reference files.');
        return;
    }

    const formData = new FormData();
    formData.append('voiceFile', voiceFile);
    formData.append('referenceFile', referenceFile);
    formData.append('serverUrl', finalUrl);

    try {
        const response = await fetch('/evaluate', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        const output = result.calculated_text; // Assuming the server returns a JSON with an 'output' field

        const formattedText = formatOutputText(output);
        document.getElementById('output-text').innerHTML = formattedText;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
});

function formatOutputText(text) {
    return text
        // Wrap the wrong word and its fix in a wrapper div
        .replace(/<([^>]+)>\s*\(([^)]+)\)/g, '<span class="fix-wrapper"><span class="fix">$2</span><span class="wrong">$1</span></span>')
        .replace(/\{([^}]+)\}/g, '<span class="insertion">$1</span>')
        // Replace deleted words with empty space equivalent to the word length
        // Replace deleted words without adding space
        .replace(/\[([^\]]+)]/g, function(match, deletionWord) {
            return `<span class="deletion-wrapper"><span class="deletion">${deletionWord}</span></span>`;
        });
}

// Handle the checkbox to show/hide the custom IP input
document.getElementById('use-custom-ip').addEventListener('change', function() {
    const customIpField = document.getElementById('custom-ip');
    if (this.checked) {
        customIpField.style.display = 'block';  // Show the custom IP input
    } else {
        customIpField.style.display = 'none';   // Hide the custom IP input
    }
});