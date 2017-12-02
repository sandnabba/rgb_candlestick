var path = require('path');

module.exports = {
	entry: {
			app: path.resolve('./src/index.js'),
			vendor: [ "mithril" ],
	},
	output: {
			filename: 'javascript/[name].bundle.js',
			chunkFilename: '[id].bundle.js',
			path: path.resolve('./build'),
			publicPath: 'public/',
	},
};
