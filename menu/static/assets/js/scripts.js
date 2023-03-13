$(() => {
    $('#year').html(new Date().getFullYear())
    $(document).on('click', '.counter .plus', (e) => {
        e.preventDefault();
        const value = $('.counter .show')
        value.html(parseInt(value.text()) + 1)
    })
    $(document).on('click', '.counter .minus', (e) => {
        e.preventDefault();
        const value = $('.counter .show')
        if (+value.text() > 0) return value.html(parseInt(value.text()) - 1)
    })
    $(document).on('click', '.actions .remove', (e) => {
        e.preventDefault();
        const parent = $(".actions .remove").parent().parent()
        confirm("Are you sure?")
        parent.remove()
    })
})