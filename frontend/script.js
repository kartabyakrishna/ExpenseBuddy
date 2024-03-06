document.addEventListener('DOMContentLoaded', function () {
    const expenseForm = document.getElementById('expenseForm');

    expenseForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(expenseForm);

        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Expense submitted successfully!');
                } else {
                    console.error('Error submitting expense:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
