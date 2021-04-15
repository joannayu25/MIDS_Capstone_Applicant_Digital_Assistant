<p><script src="https://dwl7m10czm8e.cloudfront.net/lex-web-ui-loader.min.js"></script> <script>
  var loaderOpts = {
    baseUrl: 'https://dwl7m10czm8e.cloudfront.net/',
    shouldLoadMinDeps: true
  };
  var loader = new ChatBotUiLoader.IframeLoader(loaderOpts);
var chatbotUiConfig = {
  ui: {
    parentOrigin: window.location.origin,
  },
  iframe: {
    iframeOrigin: 'https://dwl7m10czm8e.cloudfront.net',
iframeSrcPath: '/index.html#/?lexWebUiEmbed=true',
  }
};
  loader.load(chatbotUiConfig)
    .catch(function (error) { console.error(error); });


window.addEventListener('load', function () {
  var link = document.querySelector('div.wp-block-button a');
  link.href = '#';
  link.addEventListener('click', function(event) {
  event.preventDefault();
    var iframeContainerClassSelector = '.lex-web-ui-iframe';
    var iframeElement = document.querySelector(
      iframeContainerClassSelector + ' iframe'
    );
    var messageChannel = new MessageChannel();

    var message = { event: 'toggleMinimizeUi' };
    var iframeOrigin = 'https://dwl7m10czm8e.cloudfront.net';
function sendMessageToIframe(evt) {
      messageChannel.port1.close();
      messageChannel.port2.close();
      // successful message responses include the event field set to 'resolve'
      if (evt.data.event === 'resolve') {
        console.log('iframe successfully handled our message', evt.data);
      } else {
        console.error('iframe failed to handle our message', evt.data);
      }
    }

    messageChannel.port1.onmessage = sendMessageToIframe;

    iframeElement.contentWindow.postMessage(message,
      iframeOrigin, [messageChannel.port2]);
  });
});
</script></p>
