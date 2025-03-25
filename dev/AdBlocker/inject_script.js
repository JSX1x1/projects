(function () {
    "use strict";

    // Configuration: Users can modify these parameters
    const config = {
        blockedPrefixes: ["extension://gfenajajnjjmmdojhdjmnngomkhlnfjl/"], // Add more prefixes if needed
        checkInterval: 200, // Time in ms for continuous checks
        enableRedirectBlocking: true,
        enablePopupBlocking: true,
        enableMutationObserver: true,
    };

    // Instantly stop if redirected
    const stopImmediateRedirect = () => {
        config.blockedPrefixes.forEach((prefix) => {
            if (window.location.href.startsWith(prefix)) {+
                console.log("Blocked immediate redirect to: " + window.location.href);
                window.stop();
                document.documentElement.innerHTML = "<h1>Redirect Blocked</h1>";
            }
        });
    };
    stopImmediateRedirect();

    // Define a general blocker function
    const initGlobalRedirectBlocker = () => {
        if (config.enableRedirectBlocking) {
            const originalPushState = history.pushState;
            const originalReplaceState = history.replaceState;

            const stopRedirects = () => {
                config.blockedPrefixes.forEach((prefix) => {
                    if (window.location.href.startsWith(prefix)) {
                        console.log("Redirect blocked to: " + window.location.href);
                        window.stop();
                        document.documentElement.innerHTML = "<h1>Redirect Blocked</h1>";
                    }
                });
            };

            // Overwrite core methods
            history.pushState = function (...args) {
                console.log("Blocked pushState redirect");
                stopRedirects();
                return originalPushState.apply(this, args);
            };
            history.replaceState = function (...args) {
                console.log("Blocked replaceState redirect");
                stopRedirects();
                return originalReplaceState.apply(this, args);
            };

            const originalAssign = window.location.assign;
            const originalReplace = window.location.replace;

            window.location.assign = function (url) {
                if (!config.blockedPrefixes.some((prefix) => url.startsWith(prefix))) {
                    return originalAssign.call(window.location, url);
                } else {
                    console.log("Blocked location.assign to: " + url);
                }
            };
            window.location.replace = function (url) {
                if (!config.blockedPrefixes.some((prefix) => url.startsWith(prefix))) {
                    return originalReplace.call(window.location, url);
                } else {
                    console.log("Blocked location.replace to: " + url);
                }
            };
        }

        if (config.enablePopupBlocking) {
            // Overwrite open method to block popups
            const originalOpen = window.open;
            window.open = function (url, ...args) {
                if (!config.blockedPrefixes.some((prefix) => url.startsWith(prefix))) {
                    return originalOpen.apply(window, [url, ...args]);
                } else {
                    console.log("Blocked window.open redirect to: " + url);
                }
            };

            // Kill timers that might redirect or trigger popups
            const originalSetTimeout = window.setTimeout;
            const originalSetInterval = window.setInterval;

            window.setTimeout = function (fn, delay, ...args) {
                if (config.blockedPrefixes.some((prefix) => fn.toString().includes(prefix))) {
                    console.log("Blocked suspicious setTimeout");
                } else {
                    return originalSetTimeout.call(this, fn, delay, ...args);
                }
            };
            window.setInterval = function (fn, delay, ...args) {
                if (config.blockedPrefixes.some((prefix) => fn.toString().includes(prefix))) {
                    console.log("Blocked suspicious setInterval");
                } else {
                    return originalSetInterval.call(this, fn, delay, ...args);
                }
            };
        }

        // Remove suspicious iframes, scripts, and popup-related elements
        const removeSuspiciousElements = () => {
            document.querySelectorAll("iframe, script, div.popup, span.ad-popup").forEach((el) => {
                const src = el.getAttribute("src");
                if (src && config.blockedPrefixes.some((prefix) => src.startsWith(prefix))) {
                    console.log("Removed suspicious element: " + src);
                    el.remove();
                }
            });
        };

        // Continuous monitoring using setInterval
        if (config.checkInterval > 0) {
            setInterval(() => {
                if (config.enableRedirectBlocking) stopImmediateRedirect();
                if (config.enablePopupBlocking) removeSuspiciousElements();
            }, config.checkInterval);
        }

        // Dynamic monitoring using MutationObserver
        if (config.enableMutationObserver) {
            const observer = new MutationObserver(() => {
                removeSuspiciousElements();
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true,
            });
        }

        // Block click-based redirects
        document.addEventListener(
            "click",
            (event) => {
                const target = event.target.closest("a, button, [data-popup-link]");
                if (target && config.blockedPrefixes.some((prefix) => target.href.startsWith(prefix))) {
                    console.log("Blocked click redirect to: " + target.href);
                    event.preventDefault();
                }
            },
            true
        );

        console.log("Enhanced redirect and popup blocker is now globally active!");
    };

    // Inject into every page
    if (document.readyState === "complete" || document.readyState === "interactive") {
        initGlobalRedirectBlocker();
    } else {
        window.addEventListener("DOMContentLoaded", initGlobalRedirectBlocker);
    }
})();
