import '/static/menu/js/plugins/jQuery.js'
import '/static/menu/js/plugins/toastr.min.js'

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}
$(document).ready(function () {
    $(document).on('click', '.accept-order', function (e) {
        const order = $(this).data('id');
        const modal = `<div class="modal fade" id="acceptOrderModal" tabindex="-1" aria-labelledby="acceptOrderModalLabel" aria-hidden="true">
  <div class="modal-dialog">
        <form method="post" class="accept_order_form" data-id="${order}">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="acceptOrderModalLabel">Accept order #${order}</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
          <div class="mb-3">
            <label for="receive_time" class="col-form-label">Receive Time</label>
           <input type="text" id="receive_time" value="15">
           
          </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="submit" class="btn btn-primary">Accept order</button>
      </div>
        </form>
    </div>
  </div>
</div>`
        $('body').append(modal)
        $('#acceptOrderModal').modal('show')
    })
    $(document).on("hidden.bs.modal", "#acceptOrderModal", function (e) {
        $(this).remove();
    });

    $(document).on('submit', '.accept_order_form', function (e) {
        e.preventDefault();
        const receive_time = $('#receive_time').val()
        const order = $(this).data('id')
        let url = location.href.split('/')
        if (url.pop().match('[0-9]'))
            url = url.join('/')
        else url = location.href
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                receive_time,
                order,
                order_accept: true
            },
            success: function (data) {
                toastr[data?.status](data?.message)
                if (data?.status === 'success') {
                    $('#acceptOrderModal').modal('hide')
                    $(`.accept-order[data-id="${order}"]`).remove();
                    $(`.accept-order[data-id="${order}"]`).parent().remove()
                }
            }, error: function (error) {
                console.error(error)
            }
        })
    })
     if ("Notification" in window) {
        // Check if notifications are already allowed or denied
        if (Notification.permission !== "granted") {
            confirm('Please allow notification');
            // Request permission for notifications
            Notification.requestPermission().then(function (permission) {
                // If permission is granted, you can proceed with sending notifications
                if (permission !== "granted") {
                    // You can proceed with sending notifications
                   location.reload();
                }
            });
        }
    } else{
        alert("Your browser don't support notification please open anther browser")
        location.reload();
    }
});