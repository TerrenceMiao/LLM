document.getElementById('clickMe').addEventListener('click', () => {
  const messageDiv = document.getElementById('message');
  messageDiv.textContent = 'Hello! The extension is working!';
  
  // Change the message color to make it more noticeable
  messageDiv.style.color = '#4CAF50';
  
  // Optional: You can also interact with the active tab
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    // Here you can add code to interact with the current tab
    console.log('Current tab:', tabs[0]);
  });
});