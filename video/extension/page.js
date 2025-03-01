'use strict';

var youtubeURL;
var videoSummaryURL;

var isAppended = false;

function AddSummaryButton() {
  var ytpRightControls = document.getElementsByClassName("ytp-right-controls")[0];
  if (!ytpRightControls) {
    isAppended = false;
    return;
  }

  ytpRightControls.prepend(summaryButton);
  isAppended = true;
}

function GenerateVideoSummary() {
  youtubeURL = document.createElement("a");
  console.log("Youtube URL = " + youtubeURL.baseURI);

  chrome.storage.sync.get(['videoSummaryURL'], function (result) {
    if (result.videoSummaryURL === '') {
      alert("Please enter the Video Summary Backend API URL in the Options page");
    } else {
      videoSummaryURL = result.videoSummaryURL;
      console.log("Video Summary Backend API URL = " + videoSummaryURL);

      fetch(videoSummaryURL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: youtubeURL.baseURI
        })
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          // Handle the response data here
          if (data.summary) {
            console.log('Video Summary: ', data.summary);
            // Create modal to display summary
            const modal = document.createElement('div');
            modal.style.cssText = `
              background: black;
              color: white;
              padding: 10px;
              border-radius: 8px;
              overflow-y: auto;
              z-index: 10000;
              box-shadow: 0 0 10px rgba(0,0,0,0.5);
              font-family: "Roboto", "Arial", sans-serif;
              font-size: 1.4rem;
              line-height: 2rem;
            `;

            // Convert Markdown to HTML using marked
            modal.innerHTML = marked.parse(data.summary, { breaks: true });

            // Find the target element
            const secondaryInner = document.getElementById('secondary-inner');
            if (secondaryInner) {
              secondaryInner.parentNode.insertBefore(modal, secondaryInner);
            } else {
              // Fallback to body if target element not found
              document.body.appendChild(modal);
            }
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          alert('Failed to generate video summary');
        });
    }
  });
}

function onDomChange(mutationsList, observer) {
  let run = false;

  for (let mutation of mutationsList) {
    if (mutation.type === 'childList') {
      run = true;
    }
  }

  if (run) {
    let ytpRightControls = document.getElementsByClassName("ytp-right-controls")[0];
    if (ytpRightControls && isAppended === false) {
      AddSummaryButton();
    }
  }
}

var summaryButton = document.createElement("button");
summaryButton.innerHTML = "Summary";
summaryButton.className = "summaryButton ytp-button";
summaryButton.style.width = "auto";
summaryButton.style.cssFloat = "left";
summaryButton.onclick = GenerateVideoSummary;

AddSummaryButton();

const observer = new MutationObserver(onDomChange);

observer.observe(document.body, {
  childList: true,
  subtree: true
});
