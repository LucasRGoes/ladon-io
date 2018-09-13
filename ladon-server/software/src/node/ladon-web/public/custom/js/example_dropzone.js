$(function() {

	const processedPhoto 		= document.getElementById('processed_photo')
	const processedPhotoCaption = document.getElementById('processed_photo_caption')
	const uploader 		 		= new Dropzone('.dropzone')

	uploader.on('success', function(file, response) {

		processedPhoto.src = `data:image/png;base64,${ response['draw_image'] }`
		delete response['draw_image']
		processedPhotoCaption.innerHTML = JSON.stringify(response)

		// // Storing original canvas size
		// const canvasWidth  = canvas.width
		// const canvasHeigth = canvas.height

		// alert(canvasWidth)

		// // Resizing canvas to image size
		// canvas.width  = currentImage.width
		// canvas.height = currentImage.height

		// Drawing image
		// ctx.drawImage(currentImage, 0, 0)

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
