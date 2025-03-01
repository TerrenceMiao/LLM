'use strict';

chrome.storage.sync.get(['videoSummaryURL'], function (result) {
  if (result.videoSummaryURL && VideoSummaryURL.value === '') {
    VideoSummaryURL.value = result.videoSummaryURL;
  }
});

VideoSummaryURL.oninput = function () {
  chrome.storage.sync.set({ 'videoSummaryURL': this.value });
};
