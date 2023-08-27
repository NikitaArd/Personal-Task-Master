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
            <div class="item" id="${pk}">
            <p class="item-title">${fields['title']}</p>
                <div class="item-interaction">
                    <button type="submit" class="item-delete" id="delete-button" value="${pk}"></button>
                    <button type="submit" class="item-update" id="update-button" value="${pk}"></button>
                </div>
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

function ajaxUpdateRequest(url, data, elem) {
    $.ajax({
        type: 'GET',
        url: url,
        data: data,

        success: function (response) {

            var task = JSON.parse(response['task']);
            var fields = task[0]['fields'];
            var pk = task[0]['pk'];
            elem.parentElement.parentElement.remove();

            if (fields['doneStatus']) {
                $('#tasksDone').prepend(`
            <div class="item item-done" id="${pk}">
                <p class="item-title item-title-done">${fields['title']}</p>
                <div class="item-interaction">
                    <button type="submit" class="item-delete" id="delete-button" value="${pk}"></button>
                    <button type="submit" class="item-update item-update-done" id="update-button" value="${pk}"></button>
                </div>
            </div>
            `)

            } else {
                $('#tasks').prepend(`
            <div class="item" id="${pk}">
            <p class="item-title">${fields['title']}</p>
                <div class="item-interaction">
                    <button type="submit" class="item-delete" id="delete-button" value="${pk}"></button>
                    <button type="submit" class="item-update" id="update-button" value="${pk}"></button>
                </div>
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

function ajaxDeleteRequest(url, elem){
    $.ajax({
        type: 'GET',
        url: url,
        data: {},

        success: function(response){
            elem.parentElement.parentElement.remove();
            console.log(response)
            devider()
        },
        error: function(response){
            console.log(response)
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

    // check if user click on 'interactive' button
    if (Boolean($(event.target).val()) == false) return;

    requestController(event.target, 1)
});


document.getElementById('tasksDone').addEventListener('click', event => {

    // check if user click on 'interactive' button
    if (Boolean($(event.target).val()) == false) return;

    requestController(event.target, 0)
});

function requestController(elem, doneFlag){
    if ($(elem)[0]['id'] == 'delete-button'){
        var pk = $(elem).val();
        var url = `/taskapp/ajax/delete/${pk}/`;
        ajaxDeleteRequest(url, elem)
    }
    if ($(elem)[0]['id'] == 'update-button'){
        data = {
            'doneFlag': doneFlag,
        }
        var pk = $(elem).val();
        var url = `/taskapp/ajax/update/${pk}/`;

        ajaxUpdateRequest(url, data, elem);
    }
}

document.addEventListener('DOMContentLoaded', devider);

// document.getElementById('tasks').addEventListener('click', event => {
//     console.log($(event.target)[0]['id'])
//     // if (Boolean($(event.target).val()) == false) return;

//     // var pk = $(event.target).val();
//     // var url = `/taskapp/ajax/delete/${pk}`

//     // $.ajax({
//     //     type: 'GET',
//     //     data: {},
//     //     url: url,

//     //     success: function (response){
//     //         console.log(response)
//     //     },
//     //     error: function(response){
//     //         console.log(response)
//     //     },
//     // })
// })