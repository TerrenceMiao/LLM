'use strict';

var youTubeURL;
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

/**
 * Creates a YouTube Chapters like link that seek to the video specific timestamp without page reloading
 *
 * @param {string} videoId - The YouTube video ID
 * @param {string} timestamp - Timestamp in format "HH:MM:SS" or "MM:SS"
 *
 * @return {HTMLElement} - Anchor element with proper attributes
 */
function createChapterLink(videoId, timestamp) {
  // Convert timestamp to seconds
  const parts = timestamp.split(':').map(part => parseInt(part, 10));

  let seconds = 0;
  if (parts.length === 3) {
    // Format: HH:MM:SS
    seconds = parts[0] * 3600 + parts[1] * 60 + parts[2];
  } else if (parts.length === 2) {
    // Format: MM:SS
    seconds = parts[0] * 60 + parts[1];
  } else {
    // Just seconds
    seconds = parts[0];
  }

  // Create the anchor element
  const link = document.createElement('a');

  link.href = `/watch?v=${videoId}&t=${seconds}s`;
  link.textContent = timestamp;
  link.className = 'chapter-link';
  link.setAttribute('force-new-state', 'true');

  // Add click handler to prevent default navigation and handle via JS
  link.addEventListener('click', function (e) {
    e.preventDefault();

    // If using YouTube's player API
    if (window.player && typeof window.player.seekTo === 'function') {
      window.player.seekTo(seconds);
    } else {
      // Fallback: update URL without reload using History API
      const url = new URL(window.location.href);
      url.searchParams.set('t', seconds + 's');
      window.history.pushState({}, '', url);

      // If on YouTube, try to access their player
      try {
        const videoElement = document.querySelector('video');
        if (videoElement) {
          videoElement.currentTime = seconds;
        }
      } catch (err) {
        console.error('Could not seek video:', err);
      }
    }
  });

  return link;
}

function GenerateVideoSummary() {
  // Get the current played video's YouTube URL
  const youTubeURL = document.createElement("a");
  console.log("YouTube URL = " + youTubeURL.baseURI);

  // Extract video ID from YouTube URL
  const urlObj = new URL(youTubeURL.baseURI);
  const videoId = urlObj.searchParams.get('v') ||
    youTubeURL.baseURI.split('youtube.com/')[1]?.split('?')[0] ||
    '';
  console.log("YouTube Video ID = " + videoId);

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
          url: youTubeURL.baseURI
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
            // modal.innerHTML = marked.parse(data.summary, { breaks: true });

            // Create chapter links
            const chapters = [
              { time: '0:00', content: 'Introduction' },
              { time: '1:24', content: 'First Point' },
              { time: '3:45', content: 'Second Point' }
            ];

            chapters.forEach(chapter => {
              // Create a container for each chapter entry
              const chapterContainer = document.createElement('div');
              chapterContainer.style.cssText = 'display: flex; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 8px;';

              // Add YouTube Chapters like link
              const chapterLink = createChapterLink(videoId, chapter.time);
              chapterLink.style.cssText = 'color: #3ea6ff; text-decoration: none; padding: 0 8px; margin: 0; border-bottom: none;';
              chapterContainer.appendChild(chapterLink);

              // Add YouTube Chapters like content
              const chapterContent = document.createElement('div');
              chapterContent.textContent = chapter.content;
              chapterContent.style.cssText = 'color: white; padding-left: 8px; flex: 1;';
              chapterContainer.appendChild(chapterContent);

              modal.appendChild(chapterContainer);
            });

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
