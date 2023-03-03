import '/static/menu/js/plugins/jQuery.js'

$(document).ready(function () {
    $(document).on('click', '.accept-order', function (e){
        const order = $(this).parent().parent().data('id');
        const modal = `<div class="modal fade" id="acceptOrderModal" tabindex="-1" aria-labelledby="acceptOrderModalLabel" aria-hidden="true">
  <div class="modal-dialog">
        <form method="post" class="accept_order_form" data-id="${order}">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="acceptOrderModalLabel">New message</h1>
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
        <button type="submit" class="btn btn-primary">Send message</button>
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

    $(document).on('submit','.accept_order_form',function (e){
        e.preventDefault();
        console.log('e')
        const receive_time = $('#receive_time').val()
        const order = $(this).data('id')
        $.ajax({
            type:'POST',
            url:location.href,
            data:{
                receive_time,
                order,
                order_accept:true
            },
            success: function (data){
                console.log(data)
                if (data?.status === 'success') {
                    $('#acceptOrderModal').modal('hide')
                    $(`.card[data-id="${order}"]`).find(`#card-footer`).remove()
                }
            },error:function (error){
                console.error(error)
            }
        })
    })
});