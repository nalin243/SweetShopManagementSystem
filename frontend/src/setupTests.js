// 🧩 Fix TextEncoder/TextDecoder first
import { TextEncoder, TextDecoder } from "util";
if (!global.TextEncoder) global.TextEncoder = TextEncoder;
if (!global.TextDecoder) global.TextDecoder = TextDecoder;

// 🧩 Fetch / DOM polyfills
import "whatwg-fetch";
import "@testing-library/jest-dom";

// 🧩 Only now import MSW
import { server } from "./mocks/server";

// Start MSW before all tests
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
