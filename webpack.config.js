const path = require('path');

module.exports = {
    mode: 'development',
    entry: './staticfiles/JS/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'staticfiles/JS'),
    },
};

// TODO run "npx webpack --mode production" before deployment