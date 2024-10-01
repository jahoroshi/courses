let selectedForkliftId = null;
let isEditingForklift = false;
let originalForkliftData = {};
let selectedDowntimeId = null;
let isEditingDowntime = false;
let originalDowntimeData = {};

document.addEventListener('DOMContentLoaded', function() {
    toggleForkliftButtons(false);
    toggleDowntimeButtons(false);

    let forkliftRows = document.querySelectorAll('tbody tr');
    if (forkliftRows.length === 1) {
        let forkliftId = forkliftRows[0].getAttribute('data-forklift-id');
        selectForklift(null, parseInt(forkliftId));
    } else {
        clearDowntimes();
    }
});

function clearDowntimes() {
    let downtimesBody = document.getElementById('downtimesBody');
    downtimesBody.innerHTML = '';
    toggleDowntimeButtons(false);
}

function selectForklift(event, id) {
    if (event && event.target.tagName.toLowerCase() === 'input') {
        return;
    }
    if (isEditingForklift) {
        alert('Сохраните или отмените изменения перед выбором другого погрузчика.');
        return;
    }
    selectedForkliftId = id;
    highlightSelectedForkliftRow(id);

    document.getElementById('editButton').disabled = false;
    document.getElementById('deleteButton').disabled = false;

    loadDowntimes(selectedForkliftId);
    document.getElementById('addDowntimeButton').disabled = false;
}

function highlightSelectedForkliftRow(id) {
    let rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.classList.remove('selected');
    });
    let selectedRow = document.getElementById('forkliftRow_' + id);
    if (selectedRow) {
        selectedRow.classList.add('selected');
    }
}

function addForklift() {
    if (isEditingForklift) {
        alert('Сохраните или отмените текущие изменения перед добавлением нового погрузчика.');
        return;
    }
    isEditingForklift = true;
    selectedForkliftId = null;
    toggleForkliftButtons(true);

    document.getElementById('addDowntimeButton').disabled = true;

    let tbody = document.querySelector('table tbody');
    let newRow = document.createElement('tr');
    newRow.id = 'newForkliftRow';
    newRow.innerHTML = `
        <td></td>
        <td><input type="text" id="newBrand" onclick="event.stopPropagation()"></td>
        <td><input type="text" id="newNumber" onclick="event.stopPropagation()"></td>
        <td><input type="number" step="0.1" id="newCapacity" onclick="event.stopPropagation()"></td>
    `;
    tbody.prepend(newRow);
}

function editForklift() {
    if (!selectedForkliftId) {
        alert('Сначала выберите погрузчик для редактирования.');
        return;
    }
    isEditingForklift = true;
    toggleForkliftButtons(true);

    let row = document.getElementById('forkliftRow_' + selectedForkliftId);
    originalForkliftData = {
        brand: row.cells[1].innerText,
        number: row.cells[2].innerText,
        capacity: row.cells[3].innerText
    };

    row.cells[1].innerHTML = `<input type="text" id="editBrand" value="${originalForkliftData.brand}" onclick="event.stopPropagation()">`;
    row.cells[2].innerHTML = `<input type="text" id="editNumber" value="${originalForkliftData.number}" onclick="event.stopPropagation()">`;
    row.cells[3].innerHTML = `<input type="number" step="0.1" id="editCapacity" value="${originalForkliftData.capacity}" onclick="event.stopPropagation()">`;

    loadDowntimes(selectedForkliftId);
}

function saveForklift() {
    let brand, number, capacity;

    if (selectedForkliftId) {
        brand = document.getElementById('editBrand').value;
        number = document.getElementById('editNumber').value;
        capacity = document.getElementById('editCapacity').value;

        fetch(`/forklifts/edit/${selectedForkliftId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `brand=${encodeURIComponent(brand)}&number=${encodeURIComponent(number)}&capacity=${encodeURIComponent(capacity)}`
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        });
    } else {
        brand = document.getElementById('newBrand').value;
        number = document.getElementById('newNumber').value;
        capacity = document.getElementById('newCapacity').value;

        fetch(`/forklifts/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `brand=${encodeURIComponent(brand)}&number=${encodeURIComponent(number)}&capacity=${encodeURIComponent(capacity)}`
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        });
    }
}

function cancelEdit() {
    document.getElementById('confirmModal').style.display = 'block';
}

function confirmCancel() {
    if (selectedForkliftId) {
        let row = document.getElementById('forkliftRow_' + selectedForkliftId);
        row.cells[1].innerText = originalForkliftData.brand;
        row.cells[2].innerText = originalForkliftData.number;
        row.cells[3].innerText = originalForkliftData.capacity;
    } else {
        document.getElementById('newForkliftRow').remove();
    }
    isEditingForklift = false;
    toggleForkliftButtons(false);
    closeConfirmModal();
}

function closeConfirmModal() {
    document.getElementById('confirmModal').style.display = 'none';
}

function deleteForklift() {
    if (!selectedForkliftId) {
        alert('Сначала выберите погрузчик для удаления.');
        return;
    }
    if (confirm('Удалить погрузчик? Вы уверены?')) {
        fetch(`/forklifts/delete/${selectedForkliftId}`)
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            });
    }
}

function toggleForkliftButtons(editMode) {
    document.getElementById('saveButton').disabled = !editMode;
    document.getElementById('cancelButton').disabled = !editMode;
    document.getElementById('addButton').disabled = editMode;
    document.getElementById('editButton').disabled = !selectedForkliftId || editMode;
    document.getElementById('deleteButton').disabled = !selectedForkliftId || editMode;
}

function toggleDowntimeButtons(editMode) {
    document.getElementById('addDowntimeButton').disabled = !selectedForkliftId || editMode;
    document.getElementById('editDowntimeButton').disabled = !selectedDowntimeId || editMode;
    document.getElementById('deleteDowntimeButton').disabled = !selectedDowntimeId || editMode;
}

function loadDowntimes(forkliftId) {
    fetch(`/api/forklifts/${forkliftId}/downtimes`)
        .then(response => response.json())
        .then(data => {
            let downtimesBody = document.getElementById('downtimesBody');
            downtimesBody.innerHTML = '';
            data.forEach(downtime => {
                let row = createDowntimeRow(downtime);
                downtimesBody.appendChild(row);
            });
            toggleDowntimeButtons(false);
            selectedDowntimeId = null;
        });
}

function createDowntimeRow(downtime) {
    let tr = document.createElement('tr');
    tr.id = 'downtimeRow_' + downtime.id;
    tr.onclick = (event) => selectDowntime(event, downtime.id);
    tr.innerHTML = `
        <td data-value="${downtime.start_time}">${formatDateTime(downtime.start_time)}</td>
        <td data-value="${downtime.end_time || ''}">${downtime.end_time ? formatDateTime(downtime.end_time) : 'Действующий'}</td>
        <td>${downtime.reason || ''}</td>
        <td>${downtime.downtime_duration}</td>
    `;
    return tr;
}

function selectDowntime(event, id) {
    if (isEditingDowntime) {
        alert('Сохраните или отмените изменения перед выбором другого простоя.');
        return;
    }
    selectedDowntimeId = id;
    highlightSelectedDowntimeRow(id);
    document.getElementById('editDowntimeButton').disabled = false;
    document.getElementById('deleteDowntimeButton').disabled = false;
}

function highlightSelectedDowntimeRow(id) {
    let rows = document.querySelectorAll('#downtimesBody tr');
    rows.forEach(row => {
        row.classList.remove('selected');
    });
    let selectedRow = document.getElementById('downtimeRow_' + id);
    if (selectedRow) {
        selectedRow.classList.add('selected');
    }
}

function addDowntime() {
    if (isEditingDowntime) {
        alert('Сохраните или отмените текущие изменения перед добавлением нового простоя.');
        return;
    }
    if (!selectedForkliftId) {
        alert('Сначала выберите погрузчик для добавления простоя.');
        return;
    }
    isEditingDowntime = true;
    clearDowntimeModal();
    document.getElementById('downtimeModalTitle').innerText = 'Добавить простой';
    document.getElementById('downtimeStart').value = getCurrentDateTimeLocal();
    document.getElementById('downtimeModal').style.display = 'block';
}

function getCurrentDateTimeLocal() {
    let now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    return now.toISOString().slice(0,16);
}

function editDowntime() {
    if (!selectedDowntimeId) {
        alert('Сначала выберите простой для редактирования.');
        return;
    }
    isEditingDowntime = true;
    document.getElementById('downtimeModalTitle').innerText = 'Изменить простой';

    let downtime = getDowntimeById(selectedDowntimeId);
    if (downtime) {
        document.getElementById('downtimeStart').value = getInputDateTimeValue(downtime.start_time);
        document.getElementById('downtimeEnd').value = downtime.end_time ? getInputDateTimeValue(downtime.end_time) : '';
        document.getElementById('downtimeReason').value = downtime.reason || '';
        document.getElementById('downtimeModal').style.display = 'block';
    } else {
        alert('Не удалось загрузить данные простоя.');
        isEditingDowntime = false;
    }
}

function getDowntimeById(id) {
    let row = document.getElementById('downtimeRow_' + id);
    if (row) {
        let start_time = row.cells[0].getAttribute('data-value');
        let end_time = row.cells[1].getAttribute('data-value');
        let reason = row.cells[2].innerText;
        return {
            id: id,
            start_time: start_time,
            end_time: end_time,
            reason: reason,
        };
    }
    return null;
}

function getInputDateTimeValue(dateTimeStr) {
    if (!dateTimeStr) return '';
    let date = new Date(dateTimeStr);
    date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    return date.toISOString().slice(0,16);
}

function saveDowntime() {
    let startTime = document.getElementById('downtimeStart').value;
    let endTime = document.getElementById('downtimeEnd').value;
    let reason = document.getElementById('downtimeReason').value;

    if (!startTime) {
        alert('Пожалуйста, укажите начало простоя.');
        return;
    }

    let data = `forklift_id=${selectedForkliftId}&start_time=${encodeURIComponent(startTime)}&end_time=${encodeURIComponent(endTime)}&reason=${encodeURIComponent(reason)}`;

    if (isEditingDowntime && selectedDowntimeId) {
        fetch(`/downtimes/edit/${selectedDowntimeId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data
        }).then(response => {
            if (response.ok) {
                closeDowntimeModal();
                loadDowntimes(selectedForkliftId);
                isEditingDowntime = false;
                selectedDowntimeId = null;
                document.getElementById('editDowntimeButton').disabled = true;
                document.getElementById('deleteDowntimeButton').disabled = true;
            } else {
                alert('Не удалось сохранить изменения простоя.');
            }
        });
    } else {
        fetch('/downtimes/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data
        }).then(response => {
            if (response.ok) {
                closeDowntimeModal();
                loadDowntimes(selectedForkliftId);
                isEditingDowntime = false;
            } else {
                alert('Не удалось добавить простой.');
            }
        });
    }
}

function closeDowntimeModal() {
    document.getElementById('downtimeModal').style.display = 'none';
    isEditingDowntime = false;
    selectedDowntimeId = null;
    document.getElementById('editDowntimeButton').disabled = true;
    document.getElementById('deleteDowntimeButton').disabled = true;
}

function clearDowntimeModal() {
    document.getElementById('downtimeStart').value = '';
    document.getElementById('downtimeEnd').value = '';
    document.getElementById('downtimeReason').value = '';
}

function deleteDowntime() {
    if (!selectedDowntimeId) {
        alert('Сначала выберите простой для удаления.');
        return;
    }
    if (confirm('Удалить информацию о простое? Вы уверены?')) {
        fetch(`/downtimes/delete/${selectedDowntimeId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                document.getElementById('downtimeRow_' + selectedDowntimeId).remove();
                selectedDowntimeId = null;
                toggleDowntimeButtons(false);
            } else {
                alert('Не удалось удалить простой.');
            }
        });
    }
}

function formatDateTime(dateTimeStr) {
    let date = new Date(dateTimeStr);
    return date.toLocaleString('ru-RU');
}

window.onclick = function(event) {
    if (event.target == document.getElementById('confirmModal')) {
        closeConfirmModal();
    } else if (event.target == document.getElementById('downtimeModal')) {
        closeDowntimeModal();
    }
}
