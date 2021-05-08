const ChunksWebpackPlugin = require('chunks-webpack-plugin');
const path = require('path');

module.exports = [
  {
  entry: {
    si: './src/si.jsx',
    slideshow: './src/slideshow.jsx',
    gallery: './src/gallery.jsx',
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
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      name: false
    }
  },
  plugins: [new ChunksWebpackPlugin({
    outputPath: path.resolve(__dirname, `./templates/frontend`)
  })]
  },
  {
  entry: {
    receiver: './src/receiver.jsx',
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
  },
  },
];