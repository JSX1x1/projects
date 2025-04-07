(function() {
    const detectedExtensions = [];

    // Helper function to detect if a given pattern exists in the user agent string
    function checkUserAgent(extensionName, pattern) {
        try {
            if (pattern.test(navigator.userAgent)) {
                detectedExtensions.push(extensionName);
            }
        } catch (e) {
            console.error("Error checking user agent for extension:", extensionName, e);
        }
    }

    // Check for injected content scripts (check for specific global variables or modifications)
    function checkForInjectedScripts() {
        try {
            if (window.hasOwnProperty('___grecaptcha_cfg')) {
                detectedExtensions.push('reCAPTCHA Bypass Extension');
            }
            if (window.hasOwnProperty('__adblocker')) {
                detectedExtensions.push('AdBlock Extension');
            }
            if (typeof window._grammarly === 'object') {
                detectedExtensions.push('Grammarly Extension');
            }
            if (window.localStorage && localStorage.getItem('extensions_loaded')) {
                detectedExtensions.push('Possible Extension Storage');
            }
        } catch (e) {
            console.error('Error detecting injected scripts or global variables:', e);
        }
    }

    // Check for modified network activity patterns, including extension-related URL patterns
    function checkForExtensionRelatedURLs() {
        try {
            const currentUrl = window.location.href;
            if (currentUrl.includes('chrome-extension://')) {
                detectedExtensions.push('Chrome Extension URL Detected');
            }
        } catch (e) {
            console.error('Error detecting chrome-extension URL pattern:', e);
        }
    }

    // Check for browser plugin injections
    function checkForPluginChanges() {
        try {
            if (navigator.plugins && Array.from(navigator.plugins).some(plugin => plugin.name.includes('Chrome PDF Viewer'))) {
                detectedExtensions.push('Chrome PDF Viewer Plugin');
            }
        } catch (e) {
            console.error('Error detecting plugins:', e);
        }
    }

    // Dynamically check for other possible extension-related artifacts
    function checkForLocalStorageArtifacts() {
        try {
            if (localStorage && localStorage.getItem('adblock_detected') !== null) {
                detectedExtensions.push('AdBlock or AdBlocker Extension Detected');
            }
        } catch (e) {
            console.error('Error checking localStorage for extension traces:', e);
        }
    }

    // Scan the page for external iframes or script injections (often done by extensions like Tampermonkey or others)
    function checkForInjectedFrames() {
        try {
            const iframes = document.getElementsByTagName('iframe');
            for (let i = 0; i < iframes.length; i++) {
                const iframeSrc = iframes[i].src;
                if (iframeSrc.includes('chrome-extension://')) {
                    detectedExtensions.push('Injected Iframe from Chrome Extension');
                }
            }
        } catch (e) {
            console.error('Error detecting injected frames:', e);
        }
    }

    // Scan the page for any injected styles or elements
    function checkForInjectedStyles() {
        try {
            const styles = document.styleSheets;
            for (let i = 0; i < styles.length; i++) {
                if (styles[i].href && styles[i].href.includes('chrome-extension://')) {
                    detectedExtensions.push('Injected Chrome Extension CSS');
                }
            }
        } catch (e) {
            console.error('Error detecting injected styles:', e);
        }
    }

    // Run all checks and log out the detected extensions
    function detectExtensions() {
        checkUserAgent('AdBlock', /AdBlock/);
        checkUserAgent('Grammarly', /Grammarly/);
        checkUserAgent('Ghostery', /Ghostery/);
        checkUserAgent('Tampermonkey', /Tampermonkey/);
        checkUserAgent('LastPass', /LastPass/);
        checkUserAgent('Honey', /Honey/);
        checkUserAgent('Pushbullet', /Pushbullet/);

        checkForInjectedScripts();
        checkForExtensionRelatedURLs();
        checkForPluginChanges();
        checkForLocalStorageArtifacts();
        checkForInjectedFrames();
        checkForInjectedStyles();

        // Log detected extensions
        if (detectedExtensions.length > 0) {
            console.log("Detected Extensions: ", detectedExtensions);
        } else {
            console.log("No extensions detected.");
        }
    }

    // Trigger the detection
    detectExtensions();
})();
