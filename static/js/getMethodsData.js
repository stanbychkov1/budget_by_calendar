function getMethodsData() {
    const labels = [];
    const amounts = [];
  $.ajax({
            url: url,
            type: 'get',
            async: false,
            dataType: 'json',
            success: function (res) {
                for (const [key, value] of Object.entries(res.dictionary)) {
                   labels.push(key);
                   amounts.push(value['amount__sum']);
                }
            },
            error: function () {
                alert("Что-то пошло не так! Возможно, заполнены не все поля");
            }
        });
  return [labels, amounts]
}
