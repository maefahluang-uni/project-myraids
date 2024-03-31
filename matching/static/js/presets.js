// Function to fetch preset names from the server
function fetchPresetNames() {
    fetch('/matching/get_preset_names/')  // Update the URL to match your Django URL pattern
    .then(response => response.json())
    .then(data => {
        // Update the dropdown options with the received preset names
        const presetDropdown = document.getElementById('presetChoice');
        presetDropdown.innerHTML = ''; // Clear existing options
        data.forEach(presetName => {
            const option = document.createElement('option');
            option.value = presetName;
            option.textContent = presetName;
            presetDropdown.appendChild(option);
        });
    })
    .catch(error => {
        console.error('Error fetching preset names:', error);
    });
}

// Call the function to fetch preset names when the page loads
window.addEventListener('DOMContentLoaded', fetchPresetNames);

// Event listener for applying preset
document.getElementById('applyPreset').addEventListener('click', function() {
    var selectedPreset = document.getElementById('presetChoice').value;
    if (selectedPreset) {
        applyPreset(selectedPreset);
    } else {
        alert('Please select a preset.');
    }
});

// Function to apply preset
function applyPreset(selectedPreset) {
    var formData = new FormData();
    formData.append('preset_choice', selectedPreset);

    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update dropdowns with received presets data
        for (var presetName in data) {
            if (data.hasOwnProperty(presetName)) {
                var dropdown = document.getElementsByName(presetName)[0];
                if (dropdown) {
                    dropdown.innerHTML = '';
                    var choices = data[presetName];
                    choices.forEach(choice => {
                        var option = document.createElement('option');
                        option.value = choice;
                        option.textContent = choice;
                        dropdown.appendChild(option);
                    });
                }
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to get CSRF token from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
