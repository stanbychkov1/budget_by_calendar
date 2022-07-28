document.getElementById('totalPaymentAmountSum').innerHTML = updateTotal('paymentAmount')
document.getElementById('totalAccrualAmountSum').innerHTML = updateTotal('accrualAmount')
document.getElementById('totalAccrualAmountUSDSum').innerHTML = updateTotal('accrualAmountinUSD')
document.getElementById('totalPaymentAmountUSDSum').innerHTML = updateTotal('paymentAmountinUSD')

document.getElementById('Saldo').innerHTML = updateSaldo('totalAccrualAmountSum', 'totalPaymentAmountSum')
document.getElementById('SaldoUSD').innerHTML = updateSaldo('totalAccrualAmountUSDSum', 'totalPaymentAmountUSDSum')



function updateTotal(classname) {
    let table = document.getElementsByTagName("tbody")[0];
    let allrows = table.getElementsByTagName("tr");
    let rowTotal = 0
    for (i=0; i < allrows.length; i++) {
        amount = allrows[i].getElementsByClassName(classname)[0].outerText
        if (amount === ''){
            newAmount = 0
        } else{
            newAmount = Number.parseFloat(amount.replace(',', ''))
        }
        rowTotal = rowTotal + newAmount;
    }
    return rowTotal.toLocaleString('en-US')
}


function updateSaldo(firstClassName, secondClassName) {
    let firstAmount = Number.parseFloat(document.getElementById(firstClassName).textContent.replace(',', ''))
    let secondAmount = Number.parseFloat(document.getElementById(secondClassName).textContent.replace(',', ''))
    return Number(firstAmount - secondAmount).toLocaleString('en-US')
}
