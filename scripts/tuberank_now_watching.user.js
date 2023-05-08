  // ==UserScript==
  // @name        TubeRank - Now Watching
  // @namespace   Violentmonkey Scripts
  // @include     https://www.youtube.com/watch?v=*
  // @grant       GM.xmlhttpRequest
  // @version     1.0
  // @author      dbeley
  // @description 5/8/2023, 1:00:50 PM
  // ==/UserScript==
  (function () {
  var fireOnHashChangesToo    = true;
  var pageURLCheckTimer       = setInterval (
    function () {
        if (   this.lastPathStr  !== location.pathname
            || this.lastQueryStr !== location.search
            || (fireOnHashChangesToo && this.lastHashStr !== location.hash)
        ) {
            this.lastPathStr  = location.pathname;
            this.lastQueryStr = location.search;
            this.lastHashStr  = location.hash;
            gmWaitMain();
        }
    }
    , 1000
  );


  function gmWaitMain() {
    durationSpan = document.getElementsByClassName("ytp-time-duration")[0].innerHTML;
    var seconds = +(durationSpan.split(':').reduce((acc,time) => (60 * acc) + +time));
    var secondsToWait = parseInt(seconds/2);
    console.log(`New video detected, waiting ${secondsToWait} seconds to send to TubeRank`);
    setTimeout(gmMain, secondsToWait);
  };

  function gmMain () {
    let username = 'changeme';
    let password = 'changeme';
    let url = 'http://localhost:8000/en/api/now-watching/';

    let authentication = btoa(username + ":" + password);
    let url1 = window.location.href;
    let youtubeId = url1.split("watch?v=")[1].split("&list=")[0];
    console.log(`TubeRank: sending "now watching" request to ${url}${youtubeId}`);
    GM.xmlhttpRequest({
        method: 'POST',
        url: `${url}${youtubeId}`,
        headers: {
        'Accept': 'application/json',
        "Content-Type": "application/json",
        "Authorization": `Basic ${authentication}`
        }
    });
  };
  })();
