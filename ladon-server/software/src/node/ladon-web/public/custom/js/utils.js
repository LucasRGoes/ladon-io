/* Utils */

const aTagAsSubmitButton = () => {
	document.getElementById('my_form').submit()
}

const translateFeature = (feature) => {
	switch(feature) {
		case 1:
			return 'temperature'
		case 2:
			return 'humidity'
		case 3:
			return 'photo'
		case 4:
			return 'b_max'
		case 5:
			return 'a_max'
		case 6:
			return 'a_min'
		case 7:
			return 'L_median'
	}
}