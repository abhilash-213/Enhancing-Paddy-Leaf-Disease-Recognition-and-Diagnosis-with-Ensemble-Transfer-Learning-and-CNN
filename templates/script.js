const imageInput = document.getElementById('imageInput');
const predictButton = document.getElementById('predictButton');
const predictedCategory = document.getElementById('predictedCategory');
const causesList = document.getElementById('causesList');

// Function to handle image upload and prediction
predictButton.addEventListener('click', async () => {
  const imageFile = imageInput.files[0];
  if (!imageFile) {
    alert('Please select an image file to upload.');
    return;
  }

  // Convert image file to base64 format
  const imageData = await new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(imageFile);
  });

  // Send image data to the Python server for prediction
  const response = await fetch('/predict', {
    method: 'POST',
    body: JSON.stringify({ imageData }),
    headers: { 'Content-Type': 'application/json' }
  });
  const predictionData = await response.json();

  // Update the predicted category and causes
  predictedCategory.textContent = predictionData.predictedCategory;
  causesList.innerHTML = '';
  predictionData.causes.forEach(cause => {
    const listItem = document.createElement('li');
    listItem.textContent = cause;
    causesList.appendChild(listItem);
  });
});
