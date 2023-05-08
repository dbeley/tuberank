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
    , 111
  );

  function gmWaitMain() {
    console.log("TubeRank: new video detected, waiting 20 seconds");
    setTimeout(gmMain, 20000);
  };

  function gmMain () {
    let username = 'changeme';
    let password = 'changeme';
    let authentication = btoa(username + ":" + password);
    const tubeRankUrl = "https://tuberank.org/api/now-watching/";
    let url1 = window.location.href;
    const url1Splitted = url1.split("watch?v=");
    let youtubeId = url1Splitted[1];
    let url = 'http://localhost:8000/en/api/now-watching/';
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
