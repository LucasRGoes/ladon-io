/***************************************************************************
 * - BATCH INFORMATION PROCEDURES -
 * - First day until fourth: expecting UNDERMATURE;
 * - Fifth day: expecting NEARLYMATURE;
 * - Sixth day and others: expecting MATURE;
 * 
 * - MATURITY INFORMATION PROCEDURES -
 * For UNDERMATURE samples:
 * - Two days until batch ends: increase temperature;
 * - One day until batch ends: increase temperature drastically;
 * - Other cases: everything as expected;
 * 
 * For NEARLYMATURE samples:
 * - One day until batch ends: increase temperature;
 * - First and second day after batch starts: verify your storage operation;
 * - Other cases: everything as expected;
 * 
 * For MATURE samples:
 * - Two days until batch ends: decrease temperature;
 * - One day until batch ends: decrease temperature drastically;
 * - First to fourth day after batch starts: verify your storage operation;
 * - Other cases: everything as expected;
 ***************************************************************************/

const generateInformation = (maturity, batchStart, batchEnd) => {

	// The message to be built
	let message = ''

	// Turning the timestamps to moment.js dates
	batchStart = moment(batchStart)
	batchEnd = moment(batchEnd)
	const currentDate = moment()

	/* Procedures considering batch information */
	if( currentDate.isBefore(batchStart) ) {
		return 'Your batch hasn\'t started'
	}

	if( currentDate.isSameOrAfter(batchEnd) ) {
		return 'Your batch has ended'
	}

	// Storing the number of days since the batch started and the number of days to the batch ending
	const daysSinceBatchStarted = currentDate.diff(batchStart, 'days')
	const daysUntilBatchEnds    = batchEnd.diff(currentDate, 'days')

	if(daysSinceBatchStarted === 0) {
		message += 'Your batch started today, '
	} else if(daysSinceBatchStarted === 1) {
		message += 'Your batch started 1 day ago, '
	} else {
		message += `Your batch started ${ daysSinceBatchStarted } days ago, `
	}

	if(daysSinceBatchStarted >= 0 && daysSinceBatchStarted <= 3) {
		message += 'we expected your sample to be undermature. '
	} else if(daysSinceBatchStarted === 4) {
		message += 'we expected your sample to be nearly mature. '
	} else {
		message += 'we expected your sample to be mature. '
	}
	
	/* Procedures considering batch and maturity information */
	switch(maturity) {

		case 'UNDERMATURE':
			if(daysUntilBatchEnds === 2) {
				message += 'Since your sample is undermature and you have 2 days until the end of your batch, we suggest you to increase your storage temperature.'
			} else if(daysUntilBatchEnds === 1) {
				message += 'Since your sample is undermature and you have 1 day until the end of your batch, we suggest you to drastically increase your storage temperature.'
			} else {
				message += 'Your storage operation is going as expected.'
			}
			break

		case 'NEARLYMATURE':
			if(daysUntilBatchEnds === 1) {
				message += 'Since your sample is nearly mature and you have 1 day until the end of your batch, we suggest you to increase your storage temperature.'
			} else if(daysSinceBatchStarted <= 1) {
				message += 'Since your sample is nearly mature we suggest you verify your storage operation.'
			} else {
				message += 'Your storage operation is going as expected.'
			}
			break

		case 'MATURE':
			if(daysUntilBatchEnds === 2) {
				message += 'Since your sample is mature and you have 2 days until the end of your batch, we suggest you to decrease your storage temperature.'
			} else if(daysUntilBatchEnds === 1) {
				message += 'Since your sample is mature and you have 1 day until the end of your batch, we suggest you to drastically decrease your storage temperature.'
			} else if(daysSinceBatchStarted <= 3) {
				message += 'Since your sample is mature we suggest you verify your storage operation.'
			} else {
				message += 'Your storage operation is going as expected.'
			}
			break

	}

	return message 

}
