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

var isSummaryOn = false;

// Create modal to display summary
var modal;

function GenerateVideoSummary() {

  if (isSummaryOn === true) {
    modal.remove();
    isSummaryOn = false;
  }

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

            modal = document.createElement('div');
            modal.style.cssText = `
              background: #212121;
              color: white;
              padding: 12px 12px 0 12px;
              margin-bottom: 10px;
              border-radius: 8px;
              overflow-y: auto;
              z-index: 10000;
              box-shadow: 0 0 10px rgba(0,0,0,0.5);
              font-family: "Roboto", "Arial", sans-serif;
              font-size: 1.4rem;
              line-height: 2rem;
            `;

            // Create a container for the header elements to display them in one line
            const headerContainer = document.createElement('div');
            headerContainer.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin: 0 0 16px 0;';

            // Add YouTube Chapters like Summary title
            const headerSummary = document.createElement('div');
            headerSummary.textContent = 'Summary';
            headerSummary.style.cssText = 'color: white; font-family: "YouTube Sans", Roboto, sans-serif; font-size: 2rem; font-weight: 700;';
            headerContainer.appendChild(headerSummary);

            // Add YouTube Chapters like Close Button
            const headerButton = document.createElement('div');
            headerButton.innerHTML = `
              <svg xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true" style="pointer-events: none; display: inherit; width: 100%; height: 100%;">
                <path d="m12.71 12 8.15 8.15-.71.71L12 12.71l-8.15 8.15-.71-.71L11.29 12 3.15 3.85l.71-.71L12 11.29l8.15-8.15.71.71L12.71 12z" fill="white"></path>
              </svg>
            `;
            headerButton.style.cssText = 'cursor: pointer; border-radius: 50%; width: 24px; height: 24px; padding: 8px;';
            headerButton.onclick = function() {
              modal.remove();
              isSummaryOn = false;
            };
            // Add hover effect to change background color
            headerButton.addEventListener('mouseover', function() {
              this.style.backgroundColor = '#717171';
            });
            headerButton.addEventListener('mouseout', function() {
              this.style.backgroundColor = '';
            });
            headerContainer.appendChild(headerButton);

            modal.appendChild(headerContainer);

            // Convert Markdown to HTML using marked
            // modal.innerHTML = marked.parse(data.summary, { breaks: true });

            // Create chapter links
            // Parse markdown format content into chapters, e.g.:
            //
            //   [00:00:00](https://www.youtube.com/watch?v=b0XI-cbel1U&ab_channel=Fireship&t=0s)
            //   **Introduction to Grock 3**
            //   Just hours ago, a new large language model, Grock 3, was released, crushing existing benchmarks and reaching the number one spot on the LM Marina leaderboard. This model is unique in that it has direct access to the firehose of data from Twitter and is optimized for maximum truth-seeking, even if that comes at the expense of being politically correct.
            //
            //   [00:00:41](https://www.youtube.com/watch?v=b0XI-cbel1U&ab_channel=Fireship&t=41s)
            //   **AI Landscape and Competition**
            //   The AI landscape is currently ruthless, with big players like Elon Musk and Mark Zuckerberg vying for dominance. Recently, Elon attempted to troll Open AI by offering to buy it out, but the offer was rejected. Meanwhile, Mark Zuckerberg faced a setback when it was revealed that he signed off on using 82 terabytes of pirated books to train his LLaMA models.
            //
            //   [00:07:04](https://www.youtube.com/watch?v=b0XI-cbel1U&ab_channel=Fireship&t=424s)
            //   **
            //   Your 30s introduce a perfect storm of competing financial priorities, including family formation, home purchases, and career advancement. The median 30-something American earns around $53,000 but has less than $5,000 in savings while carrying over $5,500 in credit card debt. Meanwhile, the top 20% have already accumulated net worths exceeding $100,000.
            //
            //   [00:12:17](https://www.youtube.com/watch?vv=b0XI-cbel1U&ab_channel=Fireship&t=737s)
            //   **The psychological burden of retirement looms closer, creating anxiety despite higher income, but these decades offer powerful transformation opportunities, such as prioritizing aggressive debt elimination and maximizing catch-up retirement contributions.**

            // Parse the markdown into chapter objects
            const chapters = [];

            // Improved regex pattern that's more tolerant of whitespace variations
            const chapterRegex = /\[(\d{2}:\d{2}:\d{2})\](?:.*?)(?:\n|\r\n?)\s*\*{1,2}(.*?)\*{1,2}\s*(?:\n|\r\n?)([\s\S]*?)(?=\[\d{2}:\d{2}:\d{2}\]|$)/g;

            let match;
            while ((match = chapterRegex.exec(data.summary)) !== null) {
              chapters.push({
                time: match[1],
                title: (match[2].trim() === '' || match[3].trim() === '') ? '... ...' : match[2].trim(),
                content: match[3].trim() === '' ? match[2].trim() : match[3].trim()
              });
            }

            // Fallback if no chapters were parsed
            // if (chapters.length === 0) {
            //   console.warn('Failed to parse chapters from markdown, using fallback method');

            //   // Split by timestamp markers as a fallback
            //   const sections = data.summary.split(/\[\d{2}:\d{2}:\d{2}\]/);
            //   const timestamps = data.summary.match(/\[\d{2}:\d{2}:\d{2}\]/g) || [];

            //   // Skip the first section if it's empty (before first timestamp)
            //   for (let i = 1; i < sections.length; i++) {
            //     const section = sections[i].trim();
            //     const titleMatch = section.match(/\*\*(.*?)\*\*/);
            //     const title = titleMatch ? titleMatch[1].trim() : 'Section ' + i;

            //     // Get content after the title
            //     let content = section;
            //     if (titleMatch) {
            //       content = section.substring(section.indexOf(titleMatch[0]) + titleMatch[0].length).trim();
            //     }

            //     chapters.push({
            //       time: timestamps[i - 1].replace(/[\[\]]/g, ''),
            //       title: title,
            //       content: content
            //     });
            //   }
            // }

            console.log('Parsed chapters:', chapters);

            chapters.forEach(chapter => {
              // Create a container for each chapter entry
              const chapterContainer = document.createElement('div');
              chapterContainer.style.cssText = 'margin-bottom: 12px; padding-bottom: 8px;';

              // Create header container for timestamp and title
              const headerContainer = document.createElement('div');
              headerContainer.style.cssText = 'display: flex; align-items: center;';
              chapterContainer.appendChild(headerContainer);

              // Add YouTube Chapters like link
              const chapterLink = createChapterLink(videoId, chapter.time);
              chapterLink.style.cssText = 'color: #3ea6ff; background-color: #263850; text-decoration: none; padding: 0 4px; margin: 0; border-radius: 4px;';
              headerContainer.appendChild(chapterLink);

              // Add YouTube Chapters like title
              const chapterTitle = document.createElement('div');
              chapterTitle.textContent = chapter.title;
              chapterTitle.style.cssText = 'color: white; padding-left: 8px; font-weight: 500; flex: 1;';
              headerContainer.appendChild(chapterTitle);

              // Add YouTube Chapters like content on a new line
              const chapterContent = document.createElement('div');
              chapterContent.textContent = chapter.content;
              chapterContent.style.cssText = 'color: white; font-weight: 400; margin-top: 4px;';
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

            isSummaryOn = true;
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
