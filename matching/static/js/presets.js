// Function to fetch preset names from the server
function fetchPresetNames() {
    fetch('/matching/get_preset_names/') // Replace {% url "matching:get_preset_names" %} with the actual URL
    .then(response => response.json())
    .then(data => {
        const presetDropdown = document.getElementById('presetChoice');
        presetDropdown.innerHTML = ''; // Clear existing options

        // Add a null option
        const nullOption = document.createElement('option');
        nullOption.value = '';
        nullOption.textContent = 'Select Preset';
        presetDropdown.appendChild(nullOption);

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

// Function to apply preset
function applyPreset(selectedPreset) {
    var formData = new FormData();
    formData.append('preset_name', selectedPreset);

    fetch('/matching/get_preset_data/', { // Replace {% url "matching:get_preset_data" %} with the actual URL
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update dropdowns with received preset data
        for (var fieldName in data) {
            if (data.hasOwnProperty(fieldName)) {
                var dropdown = document.getElementsByName(fieldName)[0];
                if (dropdown) {
                    dropdown.innerHTML = '';
                    var choices = data[fieldName];
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
        console.error('Error applying preset:', error);
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

// Function to toggle between preset mode and non-preset mode
function toggleMode() {
    const presetDropdown = document.getElementById('presetChoice');
    const submitButton = document.querySelector('form button[type="submit"]');
    if (presetDropdown.disabled) {
        presetDropdown.disabled = false;
        submitButton.textContent = 'Save Selected Data';
    } else {
        presetDropdown.disabled = true;
        submitButton.textContent = 'Save Data';
    }
}

// Event listener for the toggle button
document.getElementById('toggleMode').addEventListener('click', toggleMode);

// Event listener for applying preset
document.getElementById('applyPreset').addEventListener('click', function() {
    var selectedPreset = document.getElementById('presetChoice').value;
    if (selectedPreset) {
        applyPreset(selectedPreset);
    } else {
        alert('Please select a preset.');
    }
});

// Event listener for DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    fetchPresetNames(); // Fetch preset names when the page loads

    const storedMapping = localStorage.getItem('userMapping');
    if (storedMapping) {
        const mapping = JSON.parse(storedMapping);
        Object.keys(mapping).forEach(function(excelColumn) {
            const selectElement = document.getElementById(excelColumn);
            if (selectElement) {
                const selectedValue = mapping[excelColumn];
                const option = selectElement.querySelector(`option[value="${selectedValue}"]`);
                if (option) {
                    option.selected = true;
                }
            }
        });
    }
});

// Function to save user mapping
function saveUserMapping() {
    const mapping = {};
    const selectElements = document.querySelectorAll('select');
    selectElements.forEach(function(selectElement) {
        const excelColumn = selectElement.id;
        const selectedValue = selectElement.value;
        mapping[excelColumn] = selectedValue;
    });
    localStorage.setItem('userMapping', JSON.stringify(mapping));
}
