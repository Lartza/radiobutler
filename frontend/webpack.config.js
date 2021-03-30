module.exports = {
  entry: {
    si: './src/si.jsx',
    slideshow: './src/slideshow.jsx',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
  }
};