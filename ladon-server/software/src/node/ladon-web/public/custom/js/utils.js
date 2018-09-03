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
	}
}