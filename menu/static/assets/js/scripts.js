$(() => {
    $('#year').html(new Date().getFullYear())
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
                console.log(data)
            }, error: function (err) {
                console.log(err)
            }
        })
    })
    $(document).on('click', '.make-order', function (e) {
        e.preventDefault();
        const order = $(this).data('id')
        const parent = $(this).parent()
        $.ajax({
            type: 'POST',
            url: `/orders/make-order`,
            data: {
                order
            },
            success: function (data) {
                parent.html(data.html)
            }, error: function (err) {
                console.log(err)
            }
        })
    })
    $(function() {
        $('#comment-form').on('submit', function(e) {
          e.preventDefault();
          var body = $('#comment-body').val();
          var order_id = '{{ order.id }}';
          $.ajax({
            url: '{% url "add_comment" %}',
            method: 'POST',
            data: {
              'order_id': order_id,
              'body': body,
              'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
              // Handle successful response here
              console.log(response);
            },
            error: function(xhr, status, error) {
              // Handle error response here
              console.log(xhr.responseText);
            }
          });
        });
      });
})
