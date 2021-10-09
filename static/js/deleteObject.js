url = '/api/accruals/delete/'
function deleteObject(id) {
    if (confirm("Вы уверены, что хотите удалить запись?")) {
        $.ajax({
            url: url + (id),
            type: 'delete',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            data: {
                'id': id,
            },
            dataType: 'json',
            success: function (data) {
                $("#objectsTable #object-" + id).remove();
            },
            error: function () {
                alert("Что-то пошло не так!");
            }
        });
       }
        return false;
}