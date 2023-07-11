module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  plugins: [
  ],
  // add your custom rules here
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/singleline-html-element-content-newline': 'off',
    'vue/multiline-html-element-content-newline': 'off',
    'eol-last': 'off',
    quotes: 'off',
    semi: 'off',
    'vue/html-self-closing': 'off',
    'space-before-function-paren': 'off',
    'vue/mustache-interpolation-spacing': 'off',
    'comma-dangle': 'off',
    'vue/max-attributes-per-line': 'off',
    'no-trailing-spaces': 'off',
    'eqeqeq': 'off',
    'arrow-parens': 'off',
    'node/handle-callback-err': 'off',
    'prefer-const': 'off',
    'vue/html-indent': 'off',
    'vue/attributes-order': 'off',
    'vue/first-attribute-linebreak': 'off',
    'vue/html-closing-bracket-newline': 'off',
    indent: 'off'
  }
}
