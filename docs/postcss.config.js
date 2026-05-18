import postcssPresetEnv from 'postcss-preset-env'

export default {
  plugins: [
    postcssPresetEnv({
      // Target browsers that support OKLch natively + generate fallbacks
      browsers: [
        'last 2 versions',
        'Safari >= 15.4',
        'not dead'
      ],
      features: {
        // Enable OKLab/OKLch color function fallbacks
        'oklab-function': true,
        'color-function': true
      },
      // Preserve the original OKLch for modern browsers
      preserve: true,
      // Enable stage 3 features (OKLch is stage 3)
      stage: 3
    })
  ]
}
