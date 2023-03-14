import '/static/menu/js/plugins/jQuery.js'
import '/static/menu/js/plugins/jQuery.cookie.js'
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
$(() => {
    function showMode() {
        const modalHtml = `<div class="modal fade " id="commentModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                              <div class="modal-dialog  modal-dialog-centered modal-dialog-scrollable">
                                <div class="modal-content bg-faded">
                                  <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel">Comments</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                  </div>
                                  <div class="modal-body" id="modal-body">
                                  </div>
                                  <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary add-comment"><i class="fa fa-add"></i> Add comment</button>
                                  </div>
                                </div>
                              </div>
                            </div>`
        $('body').append(modalHtml)

        $('#commentModal').modal('show');
    }

    $(document).on("hidden.bs.modal", "#commentModal", function (e) {
        $(this).remove();
    });
    $(document).on('click', '.counter .plus', function (e) {
        e.preventDefault();
        const value = $(this).next()
        const parent = $(this).parent().parent().parent().parent()
        const element = $(this).parent().parent();
        const order = parent.data('id')
        const item = element.data('id')
        $.ajax({
            type: 'POST',
            url: `/orders/update?op=count-plus`,
            data: {
                order: order, // assuming order is a reference to a DOM element or jQuery object
                item: item, // assuming item is a reference to a DOM element or jQuery object
            },
            success: function (data) {
                toastr[data?.status](data?.message)
                value.html(data.data.count)
            },
            error: function (err) {
                console.log(err)
            }
        });
    });
    $(document).on('click', '.counter .minus', function (e) {
        e.preventDefault();
        const value = $(this).prev()
        const parent = $(this).parent().parent().parent().parent()
        const element = $(this).parent().parent();
        const order = parent.data('id')
        const item = element.data('id')
        $.ajax({
            type: 'POST',
            url: `/orders/update?op=count-minus`,
            data: {
                order: order, // assuming order is a reference to a DOM element or jQuery object
                item: item, // assuming item is a reference to a DOM element or jQuery object
            },
            success: function (data) {
                toastr[data?.status](data?.message)
                if (data.operation === "minus")
                    return value.html(data.data.count)
                if (data.operation === "item-cancel")
                    return element.remove()
                if (data.operation === "order-cancel")
                    return parent.remove()
            },
            error: function (err) {
                console.log(err)
            }
        });
    });
    $(document).on('click', '.actions .remove', function (e) {
        e.preventDefault();
        const c = confirm("Are you sure?")
        if (!c) return;
        const parent = $(this).parent().parent().parent().parent()
        const element = $(this).parent().parent();
        const order = parent.data('id')
        const item = element.data('id')
        $.ajax({
            type: 'POST',
            url: `/orders/update?op=item-cancel`,
            data: {
                order: order, // assuming order is a reference to a DOM element or jQuery object
                item: item, // assuming item is a reference to a DOM element or jQuery object
            },
            success: function (data) {
                console.log(data)
                toastr[data?.status](data?.message)
                if (data.operation === "order-cancel")
                    return parent.remove()
            },
            error: function (err) {
                console.log(err)
            }
        });
    });
    $(document).on('click', '.order-cancel', function (e) {
        e.preventDefault();
        const c = confirm("Are you sure?")
        if (!c) return;
        const parent = $(this).parent().parent()
        const order = parent.data('id')
        $.ajax({
            type: 'POST',
            url: `/orders/update?op=order-cancel`,
            data: {
                order: order, // assuming order is a reference to a DOM element or jQuery object
            },
            success: function (data) {
                toastr[data?.status](data?.message)
                if (data.operation === "order-cancel")
                    return parent.remove()
            },
            error: function (err) {
                console.log(err)
            }
        });
    });

    $(document).on('click', '.select-item', function (e) {
        e.preventDefault();
        const itemId = $(this).data('id')
        $.ajax({
            type: 'POST',
            url: `/orders/create`,
            data: {
                itemId
            },
            success: function (data) {
                toastr[data?.status](data?.message)
            }, error: function (err) {
                console.log(err)
            }
        })
    })
    $(document).on('click', '.make-order', function (e) {
        e.preventDefault();
        const order = $(this).data('id')
        const parent = $(this).parent()
        const counter = parent.prev().find('.counter')
        $.ajax({
            type: 'POST',
            url: `/orders/make-order`,
            data: {
                order,
            },
            success: function (data) {
                toastr[data?.status](data?.message)
                $.cookie('token', data.token)
                counter.each(function () {
                    $(this).remove()
                })
                parent.html(data.html)
            }, error: function (err) {
                console.log(err)
            }
        })


    })
    $(document).on('click', '.comment', function (e) {
        e.preventDefault()
        const parent = $(this).parent().parent()
        const order = parent.data('id')
        $.ajax({
            type: 'GET',
            url: `/orders/${order}/comments`,
            success: function (data) {
                const comments = data.data
                showMode()
                $("#commentModal").data('id', order)
                if (comments) {
                    comments.map(comment => {
                        $('#modal-body').append(`<div class="bg-white p-3 mb-2">${comment.body}</div>`)
                    })
                } else {
                    $('#modal-body').html(`<div class="bg-warning p-3 text-center text-capitalize">0 Comments</div>`)
                }
            }
            , error: function (err) {
                console.error(err)
            }
        })
    })
    $(document).on('click', '.add-comment', function (e) {
        e.preventDefault()
        $('#modal-body').html(`<form>
                <label class="form-label">Comment</label>
                <textarea id="comment-body" class="form-control"></textarea>
                </form>`)
        $('.modal-footer').html(`
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary" id="comment-form-btn">Comment</button>
                                                  `)

    })
    $(document).on('click', '#comment-form-btn', function (e) {
        e.preventDefault()
        const order = $("#commentModal").data('id')
        const commentInput = $("#comment-body")
        const comment = commentInput.val()
        if (comment === '') {
            commentInput.addClass('is-invalid')
            return;
        }
        $.ajax({
            type: 'POST',
            url: `/orders/${order}/comments/create`,
            data: {
                body: comment
            },
            success: function (data) {
                toastr[data?.status](data?.message)
                const comments = data.data
                showMode()
                $("#commentModal").data('id', order)
                if (comments) {
                    $('#modal-body form').remove()
                    $('.modal-footer').html(`
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="button" class="btn btn-primary add-comment"><i class="fa fa-add"></i> Add comment</button>
                                 `)
                    comments.map(comment => {

                        $('#modal-body').prepend(`<div class="bg-white p-3 mb-2">${comment.body}</div>`)
                    })
                }
            }
            , error: function (err) {
                console.error(err)
            }
        })
    })

});