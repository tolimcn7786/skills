# Browser / JavaScript SDK

Functions compiled with the Compact compiler (`paw-4b-gpt2`) run in the browser via
WebAssembly - inference stays on the user's device.

## Install

```bash
npm install @programasweights/web
```

## Use

```javascript
import paw from '@programasweights/web';

const fn = await paw.function('email-triage-browser');
const result = await fn('Urgent: server is down!');
// result: "immediate"
```

## Notes

- Compile a browser-compatible function by passing `compiler="paw-4b-gpt2"` (from the
  Python SDK or the Playground), then load it in the browser by slug or id.
- The browser SDK resolves slugs through the PAW API, downloads browser assets, then runs
  inference client-side. Loading by **program id** keeps browser inference independent of
  the PAW API at runtime.
- Best for client-side web apps where data should not leave the device.

Canonical docs: https://programasweights.readthedocs.io
