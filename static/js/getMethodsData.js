function getMethodsData() {
    let labels = [];
    let amounts = [];
    $.ajax({
            url: '/api/methods/',
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
function getMonthlyAmountData() {
    let labels = [];
    let amounts = [];
    $.ajax({
        url: '/api/accruals_monthly/',
        type: 'get',
        async: false,
        dataType: 'json',
        success: function (res) {
            for (const [key, value] of Object.entries(res.dictionary)) {
                labels.push(key);
                amounts.push(value['amount_USD__sum']);
            }
        },
        error: function () {
            alert("Что-то пошло не так! Возможно, заполнены не все поля");
        }
    });
    return [labels, amounts]
}
