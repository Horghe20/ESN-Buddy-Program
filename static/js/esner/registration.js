const selectedInterests = [];
const selectedLanguages = [];
const selectedNationalities = [];
const selectedFaculties = [];



function selectInterest(interest) {
    const index = selectedInterests.indexOf(interest);
    if (index === -1) {
        if (selectedInterests.length < 10) {
            selectedInterests.push(interest);
        } else {
            showModal('Validation Error','Please select at most 10 interest.');
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
            showModal('Validation Error','Please select at most 5 Languages.');
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

function selectNationality(nationality) {
    if (nationality === "Not interested") {
        selectedNationalities.forEach((e) =>{
            removeNationality(e)
        })
        selectedNationalities.length = 0;
    } else {
        const index = selectedNationalities.indexOf("Not interested");
        if (index !== -1) {
            removeNationality("Not interested")
            selectedNationalities.splice(index, 1); // Remove "Not Interested" if another option is selected
        }
    }

    const index = selectedNationalities.indexOf(nationality);
    if (index === -1) {
        if (selectedNationalities.length < 3) {
            selectedNationalities.push(nationality);
        } else {
            showModal('Validation Error','Please select at most 3 nationalities.');
        }
    } else {
        selectedNationalities.splice(index, 1);
    }
    updateSelectedNationalities();
}

function updateSelectedNationalities() {
    const selectedNationalityContainer = document.getElementById('selected-nationality');
    selectedNationalityContainer.innerHTML = '';
    selectedNationalities.forEach(nationality => {
        const nationalityElement = document.createElement('div');
        nationalityElement.className = 'item selected';
        nationalityElement.innerHTML = `${nationality} <span class="remove" onclick="removeNationality('${nationality}')">x</span>`;
        selectedNationalityContainer.appendChild(nationalityElement);
    });

    // Update the nationality container to reflect the selected state
    const nationalityContainer = document.getElementById('nationality-container');
    nationalityContainer.querySelectorAll('.item').forEach(element => {
        if (selectedNationalities.includes(element.textContent.trim())) {
            element.classList.add('selected');
        } else {
            element.classList.remove('selected');
        }
    });
}

function removeNationality(nationality) {
    const index = selectedNationalities.indexOf(nationality);
    if (index !== -1) {
        selectedNationalities.splice(index, 1);
        updateSelectedNationalities();
    }
}

function selectFaculty(faculty) {
    if (faculty === "Not interested") {
        selectedFaculties.forEach((e) =>{
            removeFaculty(e)
        })
        selectedFaculties.length = 0;
    } else {
        const index = selectedFaculties.indexOf("Not interested");
        if (index !== -1) {
            removeFaculty("Not interested")
            selectedFaculties.splice(index, 1); // Remove "Not Interested" if another option is selected
        }
    }

    const index = selectedFaculties.indexOf(faculty);
    if (index === -1) {
        if (selectedFaculties.length < 3) {
            selectedFaculties.push(faculty);
        } else {
            showModal('Validation Error','Please select at most 3 Faculty.');
        }
    } else {
        selectedFaculties.splice(index, 1);
    }
    updateSelectedFaculties();
}

function updateSelectedFaculties() {
    const selectedFacultyContainer = document.getElementById('selected-faculty');
    selectedFacultyContainer.innerHTML = '';
    selectedFaculties.forEach(faculty => {
        const facultyElement = document.createElement('div');
        facultyElement.className = 'item selected';
        facultyElement.innerHTML = `${faculty} <span class="remove" onclick="removeFaculty('${faculty}')">x</span>`;
        selectedFacultyContainer.appendChild(facultyElement);
    });

    // Update the faculty container to reflect the selected state
    const facultyContainer = document.getElementById('faculty-container');
    facultyContainer.querySelectorAll('.item').forEach(element => {
        if (selectedFaculties.includes(element.textContent.trim())) {
            element.classList.add('selected');
        } else {
            element.classList.remove('selected');
        }
    });
}

function removeFaculty(faculty) {
    const index = selectedFaculties.indexOf(faculty);
    if (index !== -1) {
        selectedFaculties.splice(index, 1);
        updateSelectedFaculties();
    }
}

function validateForm() {
    if (selectedNationalities.length == 0) {
        showModal('Validation Error','Please select one Nationality');
        return false;
    }
    if (selectedFaculties.length == 0 ) {
        showModal('Validation Error','Please select one Faculty');
        return false;
    }

    if (selectedLanguages.length == 0) {
        showModal('Validation Error','Please select one Language');
        return false;
    }

    if (selectedInterests.length < 5 ) {
        showModal('Validation Error','Please select at least 5 Interest');
        return false;
    }
    return true;
}


function getData() {
    const formData = {
        name: $('#name').val(),
        surname: $('#surname').val(),
        email: $('#email').val(),
        type: $('#type').val(),
        nationality: selectedNationalities,
        languages: selectedLanguages,
        faculty: selectedFaculties,
        phone: $('#phone').val(),
        interests: selectedInterests,
        gender: $('#gender').val(),
        description: $('#description').val(),
        max_number_of_buddy: $('#max_number_of_buddy').val(),
        password: $('#password').val()
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
            url: '/esner/registration',
            data: JSON.stringify(getData()),
            contentType: 'application/json',
            success: function(response) {
                showModal("Completed", 'Form submitted successfully!')
                // Optionally, you can redirect or reset the form here
                window.location.href = "/auth/login";
            },
            error: function(error) {
                showModal("ERROR", error.responseJSON.error);
                submit_btn.prop('disabled', false);
                submit_btn.html('Submit');
            }
        });
    }
});