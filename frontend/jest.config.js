export default {
  testEnvironment: "jsdom",
  transform: { "^.+\\.[tj]sx?$": "babel-jest" },
  // 👇 let Babel process ESM-only deps
  transformIgnorePatterns: [
    "node_modules/(?!(msw|@mswjs|until-async)/)"
  ],
  moduleNameMapper: { "\\.(css|less|scss|sass)$": "identity-obj-proxy" },
  setupFiles: ["<rootDir>/jest.setup.js"],
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.js"],
};
