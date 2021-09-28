$(".createPayment").click(function() {
    var idInput = $('input[name="formId"]').val().trim();
    var patientidInput = $('input[name="formPatientId"]').val().trim();
    var dateInput = $('input[name="formDate"]').val().trim();
    var amountInput = $('input[name="formAmount"]').val().trim();
    var methodInput = $('select[name="formMethod"]').val().trim();
    if (patientidInput) {
        // Create Ajax Call
        $.ajax({
            url: '{% url "ajax_crud_create" %}',
            type: 'get',
            data: {
                'id': idInput,
                'patient_id': patientidInput,
                'date': dateInput,
                'amount': amountInput,
                'method': methodInput
            },
            dataType: 'json',
            success: function (data) {
                $("#accrualTable #accrual-" + idInput).remove();
                $('form#createPayment').trigger("reset");
                $('#myModal').modal('hide');
            },
            error: function () {
                alert("Что-то пошло не так! Возможно, заполнены не все поля");
            }
        });
       } else {
        alert("Что-то пошло не так! Возможно, заполнены не все поля");
        $('form#createPayment').trigger("reset");
        $('#myModal').modal('hide');
        return false;
    }
}
)
function precreatePayment(id, patient_id, amount) {
  if (id) {
      tr_id = "#accrual-" + id;
      patient = $(tr_id).find(".accrualPatient").text();
      date = $(tr_id).find(".accrualDate").text();
    $('#form-id').val(id);
    $('#form-patient-id').val(patient_id);
    $('#form-patient').val(patient);
    $('#form-date-session').val(date);
    $('#form-amount').val(amount);
  }
}
