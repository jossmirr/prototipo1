// core/static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    console.log('Found delete buttons:', deleteButtons.length);
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = button.getAttribute('data-url');
            const message = button.getAttribute('data-message');
            const entityType = button.getAttribute('data-entity');
            const csrfInput = document.querySelector('#csrf-form input[name="csrfmiddlewaretoken"]');
            if (!csrfInput || !csrfInput.value) {
                console.error('CSRF token not found in #csrf-form');
                alert('Error: No se pudo encontrar el token CSRF. Por favor, recarga la página.');
                return;
            }
            const csrfToken = csrfInput.value;
            console.log('URL:', url);
            console.log('Message:', message);
            console.log('Entity Type:', entityType);
            console.log('CSRF Token Length:', csrfToken.length, 'Token:', csrfToken);
            if (csrfToken.length !== 64) {
                console.error('Invalid CSRF token length:', csrfToken.length);
                alert('Error: El token CSRF tiene una longitud inválida. Por favor, recarga la página.');
                return;
            }
            if (confirm(`¿Estás seguro de eliminar el ${entityType} ${message}?`)) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = url;
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);
                document.body.appendChild(form);
                console.log('Submitting form to:', url);
                form.submit();
            }
        });
    });
});