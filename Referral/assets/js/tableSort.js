const table = document.getElementById('sortMe');
// Query the headers
const headers = table.querySelectorAll('th');

// Loop over the headers
[].forEach.call(headers, function (header, index) {
    header.addEventListener('click', function () {
        // This function will sort the column
        sortColumn(index);
    });
});
const tableBody = table.querySelector('tbody');
const rows = tableBody.querySelectorAll('tr');



const transform = function (index, content) {
    // Get the data type of column
    const type = headers[index].getAttribute('data-type');
    switch (type) {
        case 'number_int':
            return parseInt(content);
        case 'number_float':
            return parseFloat(content);
        case 'release_year':
            if (content == 'N/A') {
                return 1000;
            }
            var release_date = content.split("(")[0].trim();
            var release_year = release_date.substr(release_date.length - 4);
            return parseInt(release_year);
        case 'string':
        default:
            return content;
    }
};



const directions = Array.from(headers).map(function (header) {
    return '';
});

const sortColumn = function (index) {
    // Get the current direction
    const direction = directions[index] || 'asc';

    // A factor based on the direction
    const multiplier = (direction === 'asc') ? 1 : -1;

    const newRows = Array.from(rows);

    newRows.sort(function (rowA, rowB) {
        const cellA = rowA.querySelectorAll('td')[index].innerHTML;
        const cellB = rowB.querySelectorAll('td')[index].innerHTML;

        const a = transform(index, cellA);
        const b = transform(index, cellB);

        switch (true) {
            case a > b: return 1 * multiplier;
            case a < b: return -1 * multiplier;
            case a === b: return 0;
        }
    });

    [].forEach.call(rows, function (row) {
        tableBody.removeChild(row);
    });

    // Append new row
    newRows.forEach(function (newRow) {
        tableBody.appendChild(newRow);
    });

    // Reverse the direction
    directions[index] = direction === 'asc' ? 'desc' : 'asc';

};
