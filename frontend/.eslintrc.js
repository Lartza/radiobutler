module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'airbnb',
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
  ],
  rules: {
    "camelcase": [
      "error",
      {
        "ignoreDestructuring": true
      }
    ],
    "jsx-a11y/label-has-associated-control": [ 2, {
      "assert": "either",
    }],
  },
};
