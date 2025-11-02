// --- Browser/Node polyfills for Jest + MSW ---

import { TextEncoder, TextDecoder } from "util";
if (!global.TextEncoder) global.TextEncoder = TextEncoder;
if (!global.TextDecoder) global.TextDecoder = TextDecoder;

// 🧩 Polyfill BroadcastChannel for MSW
if (typeof global.BroadcastChannel === "undefined") {
  class BroadcastChannelPolyfill {
    constructor() {}
    postMessage() {}
    close() {}
    addEventListener() {}
    removeEventListener() {}
  }
  global.BroadcastChannel = BroadcastChannelPolyfill;
}

// 🧩 Web Streams / Fetch APIs (for Node ≥18)
const { fetch, Headers, Request, Response, ReadableStream, WritableStream, TransformStream } = globalThis;
if (!global.fetch) global.fetch = fetch;
if (!global.Headers) global.Headers = Headers;
if (!global.Request) global.Request = Request;
if (!global.Response) global.Response = Response;
if (!global.ReadableStream) global.ReadableStream = ReadableStream;
if (!global.WritableStream) global.WritableStream = WritableStream;
if (!global.TransformStream)
  global.TransformStream = class {
    readable = new ReadableStream();
    writable = new WritableStream();
  };
