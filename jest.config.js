'use strict';

module.exports = {
  testEnvironment: 'node',
  collectCoverage: false,
  collectCoverageFrom: ['cdk/*.js'],
  coveragePathIgnorePatterns: ['/node_modules/', './*.config.js', '/cdk/app.js'],
  coverageDirectory: 'reports/sonar',
  coverageReporters: ['lcov', 'text'],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  testMatch: ['**/*.test.js'],
  moduleFileExtensions: ['js', 'json'],
};
