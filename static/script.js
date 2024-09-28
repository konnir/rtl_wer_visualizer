document.getElementById('voice-file-btn').addEventListener('click', () => {
    document.getElementById('voice-file-input').click();
});

// When voice file is selected, change button color to blue
document.getElementById('voice-file-input').addEventListener('change', function() {
    const voiceFileBtn = document.getElementById('voice-file-btn');
    if (this.files.length > 0) {
        voiceFileBtn.style.backgroundColor = 'blue';  // Change to blue when file is selected
    } else {
        voiceFileBtn.style.backgroundColor = '';  // Reset to default if no file
    }
});


document.getElementById('reference-file-btn').addEventListener('click', () => {
    document.getElementById('reference-file-input').click();
});

// When reference file is selected, change button color to blue
document.getElementById('reference-file-input').addEventListener('change', function() {
    const referenceFileBtn = document.getElementById('reference-file-btn');
    if (this.files.length > 0) {
        referenceFileBtn.style.backgroundColor = 'blue';
    } else {
        referenceFileBtn.style.backgroundColor = '';
    }
});


document.getElementById('hypothesis-file-btn').addEventListener('click', () => {
    document.getElementById('hypothesis-file-input').click();
});

// When hypothesis file is selected
document.getElementById('hypothesis-file-input').addEventListener('change', function() {
    const hypothesisFileBtn = document.getElementById('hypothesis-file-btn');
    if (this.files.length > 0) {
        hypothesisFileBtn.style.backgroundColor = 'blue';
    } else {
        hypothesisFileBtn.style.backgroundColor = '';
    }
});

document.getElementById('check-btn').addEventListener('click', async () => {
    // Clear the screen
    document.getElementById('output-text').innerHTML = '';

    const voiceFile = document.getElementById('voice-file-input').files[0];
    const referenceFile = document.getElementById('reference-file-input').files[0];
    const hypothesisFile = document.getElementById('hypothesis-file-input').files[0];
    const useCustomIp = document.getElementById('use-custom-ip').checked;
    const customIp = document.getElementById('custom-ip').value;
    const serverUrl = document.getElementById('server-url').value;

    // Determine whether to use the custom IP or the selected server URL
    const finalUrl = useCustomIp && customIp ? customIp : serverUrl;

    if (!referenceFile || (!voiceFile && !hypothesisFile)) {
        alert('Please select reference with voice or hypothesis files.');
        return;
    }

    const formData = new FormData();
    if (voiceFile) formData.append('voiceFile', voiceFile);  // Only append if not null
    formData.append('referenceFile', referenceFile);  // Required
    formData.append('serverUrl', finalUrl);  // Required
    if (hypothesisFile) formData.append('hypothesisFile', hypothesisFile);  // Only append if not null

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