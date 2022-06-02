module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? '/static/dist/' : 'http://127.0.0.1:8080',
    outputDir: '../server/static/dist',

    // relative to outputDir!
    indexPath: '../../templates/base-vue.html',

    chainWebpack: config => {
        /*
        The arrow function in writeToDisk(...) tells the dev server to write
        only index.html to the disk.

        The indexPath option (see above) instructs Webpack to also rename
        index.html to base-vue.html and save it to Django templates folder.

        We don't need other assets on the disk (CSS, JS...) - the dev server
        can serve them from memory.

        See also:
        https://cli.vuejs.org/config/#indexpath
        https://webpack.js.org/configuration/dev-server/#devserverwritetodisk-
        */
        config.plugin('VuetifyLoaderPlugin').tap(args => [{
          progressiveImages: true,
          match (originalTag, { kebabTag, camelTag, path, component }) {
            if (kebabTag.startsWith('core-')) {
              return [camelTag, `import ${camelTag} from '@/components/core/${camelTag.substring(4)}.vue'`]
            }
          }
        }])
        config.devServer
            .public('http://127.0.0.1:8080')
            .hotOnly(true)
            .headers({"Access-Control-Allow-Origin": "*"})
            .writeToDisk(filePath => filePath.endsWith('index.html'));
    },

    transpileDependencies: [
      'vuetify'
    ]
}
