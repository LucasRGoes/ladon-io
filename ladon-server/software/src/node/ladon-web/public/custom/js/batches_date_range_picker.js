$(function () {

	let firstCallback = false

    const start = moment().subtract(29, 'days')
    const end = moment()

    const cb = (start, end) => {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'))

        if(firstCallback) {
	    	$('#from').val(start)
	    	$('#to')  .val(end)
	    	$('#batch_range').submit()
    	} else {
    		firstCallback = true
    	}

    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb)

    cb(start, end)

})
