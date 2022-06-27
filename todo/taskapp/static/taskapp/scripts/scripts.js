$('#add_form').submit(function (e) {
    e.preventDefault();

    var serData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: 'taskapp/ajax/create/',
        data: serData,

        success: function (response) {
            $('#add_form').trigger('reset')

            var formData = JSON.parse(response['formData'])
            var fields = formData[0]['fields']
            var pk = formData[0]['pk']
            $('#tasks').prepend(`
            <div class="item" id='${pk}'>
                <p class="item-title">${fields['title']}</p>
                <button type="submit" class="item-button" value='${pk}'></button>
            </div>
            `)
            devider();
            // var tasks = document.getElementById('tasks');
            // tasks.insertAdjacentHTML('afterbegin', `
            // <div class="item" id='${pk}'>
            //     <p class="item-title">${fields['title']}</p>
            //     <button type="submit" class="item-button" value='${pk}'></button>
            // </div>
            // `)
        },
        error: function (response) {
            alert('Error')
        }
    })
})

function ajaxRequest(url, data, elem) {
    $.ajax({
        type: 'GET',
        url: url,
        data: data,

        success: function (response) {

            var task = JSON.parse(response['task']);
            var fields = task[0]['fields'];
            var pk = task[0]['pk'];
            elem.parentElement.remove();

            if (fields['doneStatus']) {
                $('#tasksDone').prepend(`
                <div class="item item-done" id="${pk}">
                    <p class="item-title item-title-done">${fields['title']}</p>
                    <button type="submit" class="item-button item-button-done" value="${pk}"></button>
                </div>
            `)

            } else {
                $('#tasks').prepend(`
            <div class="item" id='${pk}'>
                <p class="item-title">${fields['title']}</p>
                <button type="submit" class="item-button" value='${pk}'></button>
            </div>
            `)
            }
            devider();
        },
        error: function (response) {
            alert('Error');
        }
    })
}

function devider() {
    if ($('#tasks').children().length == 0) {
        $('#first').addClass('disp-none').removeClass('disp');
    } else {
        $('#first').addClass('disp').removeClass('disp-none');
    }

    if ($('#tasksDone').children().length == 0) {
        $('#second').addClass('disp-none').removeClass('disp');
    } else {
        $('#second').addClass('disp').removeClass('disp-none');
    }
}

document.getElementById('tasks').addEventListener('click', event => {

    if (Boolean($(event.target).val()) == false) return;

    data = {
        'doneFlag': 1,
    }
    var pk = $(event.target).val();
    var url = '/taskapp/ajax/update/' + pk;

    ajaxRequest(url, data, event.target);
});

document.getElementById('tasksDone').addEventListener('click', event => {

    if (Boolean($(event.target).val()) == false) return;

    data = {
        'doneFlag': 0,
    }
    var pk = $(event.target).val();
    var url = '/taskapp/ajax/update/' + pk;

    ajaxRequest(url, data, event.target);
});

document.addEventListener('DOMContentLoaded', devider);