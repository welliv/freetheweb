/**
 * FreeTheWeb — Chatwoot Integration
 * Adds live customer support chat widget to any site
 * 
 * Usage: Include this script in any generated website
 * The agent configures the website_token and inbox_id
 */

function initChatwoot(config) {
  const {
    websiteToken = '',
    baseUrl = 'https://app.chatwoot.com',
    launcherTitle = 'Chat with us',
    position = 'right',
    darkMode = false,
    greeting = 'Hi! How can we help you today?',
  } = config;

  // Set Chatwoot configuration
  window.chatwootSettings = {
    position: position,
    type: 'standard',
    launcherTitle: launcherTitle,
    darkMode: darkMode,
  };

  // Inject Chatwoot SDK
  const script = document.createElement('script');
  script.src = `${baseUrl}/packs/js/sdk.js`;
  script.async = true;
  script.onload = function() {
    window.chatwootSDK.run({
      websiteToken: websiteToken,
      baseUrl: baseUrl,
    });
    
    // Set greeting message
    if (greeting) {
      setTimeout(() => {
        if (window.$chatwoot) {
          window.$chatwoot.toggleBubbleVisibility('show');
        }
      }, 2000);
    }
  };
  document.head.appendChild(script);
}

// Export for use
if (typeof module !== 'undefined') {
  module.exports = { initChatwoot };
}
