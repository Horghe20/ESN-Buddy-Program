const selectedInterests = [];
const selectedLanguages = [];
const selectedNationalities = [];
const selectedFaculties = [];

function selectInterest(interest) {
    const index = selectedInterests.indexOf(interest);
    if (index === -1) {
        if (selectedInterests.length < 15) {
            selectedInterests.push(interest);
        } else {
            showModal('Validation Error','Please select at most 15 interest.');
        }
    } else {
        selectedInterests.splice(index, 1);
    }
    updateSelectedInterests();
}

function updateSelectedInterests() {
    const selectedInterestsContainer = document.getElementById('selected-interests');
    selectedInterestsContainer.innerHTML = '';
    selectedInterests.forEach(interest => {
        const interestElement = document.createElement('div');
        interestElement.className = 'item selected';
        interestElement.innerHTML = `${interest} <span class="remove" onclick="removeInterest('${interest}')">x</span>`;
        selectedInterestsContainer.appendChild(interestElement);
    });

    // Update the interests container to reflect the selected state
    const interestsContainer = document.getElementById('interests-container');
    interestsContainer.querySelectorAll('.item').forEach(element => {
        if (selectedInterests.includes(element.textContent.trim())) {
            element.classList.add('selected');
        } else {
            element.classList.remove('selected');
        }
    });
}

function removeInterest(interest) {
    const index = selectedInterests.indexOf(interest);
    if (index !== -1) {
        selectedInterests.splice(index, 1);
        updateSelectedInterests();
    }
}

function selectLanguage(language) {
    const index = selectedLanguages.indexOf(language);
    if (index === -1) {
        if (selectedLanguages.length < 5) {
            selectedLanguages.push(language);
        } else {
            showModal('Validation Error','Please select at most 5 languages.');
        }
    } else {
        selectedLanguages.splice(index, 1);
    }
    updateSelectedLanguages();
}

function updateSelectedLanguages() {
    const selectedLanguagesContainer = document.getElementById('selected-languages');
    selectedLanguagesContainer.innerHTML = '';
    selectedLanguages.forEach(language => {
        const languageElement = document.createElement('div');
        languageElement.className = 'item selected';
        languageElement.innerHTML = `${language} <span class="remove" onclick="removeLanguage('${language}')">x</span>`;
        selectedLanguagesContainer.appendChild(languageElement);
    });

    // Update the languages container to reflect the selected state
    const languagesContainer = document.getElementById('languages-container');
    languagesContainer.querySelectorAll('.item').forEach(element => {
        if (selectedLanguages.includes(element.textContent.trim())) {
            element.classList.add('selected');
        } else {
            element.classList.remove('selected');
        }
    });
}

function removeLanguage(language) {
    const index = selectedLanguages.indexOf(language);
    if (index !== -1) {
        selectedLanguages.splice(index, 1);
        updateSelectedLanguages();
    }
}


function validateForm() {
    const form = document.getElementById('buddy-form');
    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }

    if (selectedLanguages.length == 0) {
        showModal('Validation Error','select at least 1 language.');
        return false;
    }

    if (selectedInterests.length == 0) {
        showModal('Validation Error','Select at least 5 interest');
        return false;
    }

    return true;
}

function getData() {
    faculty = []
    nationality = []
    faculty.push($('#faculty').val())
    nationality.push($('#nationality').val())
    const formData = {
        name: $('#name').val(),
        surname: $('#surname').val(),
        email: $('#email').val(),
        nationality: nationality,
        languages: selectedLanguages,
        faculty: faculty,
        phone: $('#phone').val(),
        instagram: $('#instagram').val(),
        telegram: $('#telegram').val(),
        interests: selectedInterests,
        gender: $('#gender').val(),
        description: $('#description').val(),
        semester: $('#semester').val(),
        year: $('#year').val()
    };
    return formData;
}

document.getElementById('buddy-form').addEventListener('submit', function(event) {
    event.preventDefault();
    if (validateForm()) {
        const submit_btn = $("#submit-btn");
        submit_btn.prop('disabled', true);
        submit_btn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...');


        $.ajax({
            type: 'POST',
            url: '/buddy/registration',
            data: JSON.stringify(getData()),
            contentType: 'application/json',
            success: function(response) {
                showModal("Completed", 'Form submitted successfully!')
                // Optionally, you can redirect or reset the form here
                submit_btn.html('Submit');

            },
            error: function(error) {
                console.log(error)
                showModal("ERROR", error.responseJSON.error)
                submit_btn.prop('disabled', false);
                submit_btn.html('Submit');
            }
        });
    }
});