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
                   amounts.push(value);
                }
            },
            error: function () {
                alert("Что-то пошло не так!");
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
                amounts.push(value);
            }
        },
        error: function () {
            alert("Что-то пошло не так!");
        }
    });
    return [labels, amounts]
}
