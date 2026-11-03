#!/bin/bash
exec /opt/pw-browsers/chromium-1243/chrome-linux64/chrome --no-sandbox --ignore-certificate-errors --proxy-server=${HTTPS_PROXY} --proxy-bypass-list="cdn.jsdelivr.net" --host-resolver-rules="MAP cdn.jsdelivr.net 127.0.0.1:8443" "$@"
