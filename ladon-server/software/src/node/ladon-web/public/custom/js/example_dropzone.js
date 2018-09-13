$(function() {

	Dropzone.autoDiscover = false

	const processedPhoto 		= document.getElementById('processed_photo')
	const processedPhotoCaption = document.getElementById('processed_photo_caption')
	const uploader 		 		= new Dropzone('.dropzone')

	const tempDrawing 			= document.getElementById('temp_drawing')
	tempDrawing.style.display   = 'none'
	const context 				= tempDrawing.getContext("2d")

	const drawText = (ctx, x, y, message) => {
		ctx.font 	  = '20px Georgia'
		ctx.fillStyle = '#000000'

		const textWidth = ctx.measureText(message).width

		ctx.fillText(message, x - (textWidth / 2), y)
	}

	context.font 		 = '40pt Georgia'
	context.textAlign 	 = 'center'
	context.textBaseline = 'middle'
	context.fillStyle 	 = '#000000'

	uploader.on('success', async function(file, response) {

		// Stores processed photo on an image class
		const processedPhotoSource = new Image()
		processedPhotoSource.src = `data:image/png;base64,${ response['draw_image'] }`
		delete response['draw_image']

		// Verifying response
		if(response !== 'File too big for processing at our test pipeline!') {

			// Resizing canvas to image size
			context.canvas.width  = processedPhotoSource.width
			context.canvas.height = processedPhotoSource.height

			// Drawing image
			context.drawImage(processedPhotoSource, 0, 0)

			// Storing centers
			centerX = response['center_x']
			delete response['center_x']
			centerY = response['center_y']
			delete response['center_y']

			// For each found sample, classify it
			const numberProcessedSamples = centerX.length
			for(let i = 0; i < numberProcessedSamples; i++) {

				const classification = await requestClassification({
					'b_max': response['b_max'][i],
					'a_max': response['a_max'][i],
					'a_min': response['a_min'][i],
					'L_median': response['l_median'][i]
				})

				drawText(context, centerX[i], centerY[i], classification['maturity'])

			}

			// Setting canvas image to image tag
			processedPhoto.src 				= tempDrawing.toDataURL()
			processedPhotoCaption.innerHTML = JSON.stringify(response)
 
		} else {
			processedPhoto.src 				= ''
			processedPhotoCaption.innerHTML = response
		}

	})

})
