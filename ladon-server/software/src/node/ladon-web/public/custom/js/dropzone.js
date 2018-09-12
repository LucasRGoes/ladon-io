$(function() {

	const canvas   = document.getElementById('processed_file')
	const ctx      = canvas.getContext("2d")
	const uploader = new Dropzone('.dropzone')

	uploader.on('success', function(file, response) {

		const currentImage = new Image()
		currentImage.src = `data:image/png;base64,${ response['draw_image'] }`

		// // Storing original canvas size
		// const canvasWidth  = canvas.width
		// const canvasHeigth = canvas.height

		// alert(canvasWidth)

		// // Resizing canvas to image size
		// canvas.width  = currentImage.width
		// canvas.height = currentImage.height

		// Drawing image
		ctx.drawImage(currentImage, 0, 0)

		// // Drawing each circle
		// const numberProcessedSamples = response['center_x'].length
		// for(let i; i < numberProcessedSamples; i++) {
		// 	ctx.beginPath()
		// 	ctx.arc( response['center_x'][i], response['center_y'][i], 50, 0, 2 * Math.PI, false )
		// 	ctx.fillStyle = 'green'
		// 	ctx.fill()
		// 	ctx.lineWidth = 5
		// 	ctx.strokeStyle = '#003300'
		// 	ctx.stroke()
		// }

		// // Redrawing canvas to original size
		// ctx.drawImage(canvas, 0, 0, canvasWidth canvasHeigth)

	})

})