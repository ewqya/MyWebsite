document.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    fetch('/register', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.querySelector('#result').innerHTML = data;
    });
});
