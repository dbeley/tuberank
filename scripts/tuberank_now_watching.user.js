  // ==UserScript==
  // @name        TubeRank - Now Watching
  // @namespace   Violentmonkey Scripts
  // @include     https://www.youtube.com/*
  // @grant       GM_xmlhttpRequest
  // @version     1.1
  // @author      dbeley
  // @description 5/8/2023, 1:00:50 PM
  // ==/UserScript==
  (function () {
  let username = 'changeme';
  let password = 'changeme';
  let url = 'https://tuberank.org/en/api/now-watching/';
  let fireOnHashChangesToo = true;
  let timer;

  function checkAndRunScript() {
    let currentURL = window.location.href;
    if (currentURL.includes('watch?v=')) {
      let durationSpan = document.getElementsByClassName("ytp-time-duration")[0];
      if (durationSpan) {
        let seconds = +(durationSpan.innerHTML.split(':').reduce((acc, time) => (60 * acc) + +time));
        let secondsToWait = parseInt(seconds / 4);
        console.log(`New video detected, waiting ${secondsToWait} seconds to send to TubeRank`);
        clearTimeout(timer);
        timer = setTimeout(gmMain, secondsToWait * 1000);
      }
    }
  }

  function gmMain() {
    let authentication = btoa(username + ":" + password);
    let url1 = window.location.href;
    let youtubeId = url1.split("watch?v=")[1].split("&")[0];
    console.log(`TubeRank: sending "now watching" request to ${url}${youtubeId}`);
    GM_xmlhttpRequest({
      method: 'POST',
      url: `${url}${youtubeId}`,
      headers: {
        'Accept': 'application/json',
        "Content-Type": "application/json",
        "Authorization": `Basic ${authentication}`
      }
    });
  }

  setInterval(function () {
    if (   this.lastPathStr !== location.pathname
        || this.lastQueryStr !== location.search
        || (fireOnHashChangesToo && this.lastHashStr !== location.hash)
    ) {
      this.lastPathStr = location.pathname;
      this.lastQueryStr = location.search;
      this.lastHashStr = location.hash;
      checkAndRunScript();
    }
  }, 5000);

})();
